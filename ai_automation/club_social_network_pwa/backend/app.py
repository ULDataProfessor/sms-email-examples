import os
from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, DateTime,
                        create_engine, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from prometheus_client import Counter, generate_latest
from fastapi_utils.tasks import repeat_every

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./club.db")
JWT_SECRET = os.getenv("JWT_SECRET", "secret")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Simple redis connection for caching open status
try:
    import redis
    redis_client = redis.from_url(REDIS_URL)
except Exception:  # pragma: no cover - optional redis
    redis_client = None

app = FastAPI(title="Campus Club Connect")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Prometheus metrics
http_requests_total = Counter('http_requests_total', 'HTTP requests total', ['endpoint'])

# --------------------- Database Models ----------------------
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Club(Base):
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    open_hours = Column(String)
    is_open = Column(Boolean, default=False)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey('clubs.id'))
    name = Column(String)
    start_time = Column(DateTime)

class Discount(Base):
    __tablename__ = 'discounts'
    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey('clubs.id'))
    description = Column(String)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Ad(Base):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    media_url = Column(String)
    active = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)

# --------------------- Schemas ----------------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    username: str
    password: str

class ClubSchema(BaseModel):
    id: int
    name: str
    description: str
    open_hours: str
    is_open: bool

    class Config:
        orm_mode = True

class AdSchema(BaseModel):
    id: int
    title: str
    media_url: str
    active: bool

    class Config:
        orm_mode = True

# --------------------- Utils ----------------------
def create_token(data: dict, expires_minutes: int = 60) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

def get_current_user(token: str = Depends(oauth_scheme)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid auth token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid auth token")
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# --------------------- Routes ----------------------
@app.post("/auth/register", response_model=Token)
def register(user: UserCreate):
    db = SessionLocal()
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    token = create_token({"sub": user.username})
    db.close()
    http_requests_total.labels(endpoint="register").inc()
    return {"access_token": token}

@app.post("/auth/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(User).filter(User.username == form.username, User.password == form.password).first()
    db.close()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_token({"sub": user.username})
    http_requests_total.labels(endpoint="login").inc()
    return {"access_token": token}

@app.get("/clubs", response_model=List[ClubSchema])
def list_clubs():
    db = SessionLocal()
    clubs = db.query(Club).all()
    db.close()
    http_requests_total.labels(endpoint="clubs").inc()
    return clubs

@app.get("/clubs/{club_id}", response_model=ClubSchema)
def get_club(club_id: int):
    db = SessionLocal()
    club = db.query(Club).get(club_id)
    db.close()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    http_requests_total.labels(endpoint="club_detail").inc()
    return club

@app.get("/ads", response_model=List[AdSchema])
def get_ads():
    db = SessionLocal()
    ads = db.query(Ad).filter(Ad.active == True).all()
    db.close()
    http_requests_total.labels(endpoint="ads_get").inc()
    return ads

@app.post("/ads", response_model=AdSchema)
def create_ad(ad: AdSchema, user: User = Depends(get_current_user)):
    db = SessionLocal()
    db_ad = Ad(title=ad.title, media_url=ad.media_url, active=ad.active)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    db.close()
    http_requests_total.labels(endpoint="ads_post").inc()
    return db_ad

# --------------------- WebSocket Chat ----------------------
class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/messages")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --------------------- Metrics ----------------------
@app.get("/metrics")
def metrics():
    return generate_latest()

# --------------------- Background Task ----------------------
@app.on_event("startup")
@repeat_every(seconds=60)
def update_open_flags() -> None:
    db = SessionLocal()
    clubs = db.query(Club).all()
    now = datetime.utcnow().hour
    for c in clubs:
        c.is_open = str(now) in (c.open_hours or '')
        if redis_client:
            redis_client.set(f"club:{c.id}:open", "1" if c.is_open else "0")
    db.commit()
    db.close()
