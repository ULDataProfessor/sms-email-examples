import React, { useEffect, useRef, useState } from 'react';

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/messages');
    ws.current.onmessage = evt => setMessages(m => [...m, evt.data]);
    return () => ws.current.close();
  }, []);

  const send = text => {
    ws.current.send(text);
  };

  return (
    <div>
      <div>{messages.map((m, i) => <div key={i}>{m}</div>)}</div>
      <button onClick={() => send('hello')}>Send</button>
    </div>
  );
}
