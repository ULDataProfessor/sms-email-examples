---
---

# SMS Web Application

The [main.py](../main.py) file is a small Flask web app that sends jokes or advice to a phone number you enter on the page.

```bash
python main.py
```

Open your browser to `http://localhost:8080/` and explore the form-driven interface.

## Key Code
```python
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        phone_number = request.form["phone_number"]
        joke = get_joke()
        advice = get_advice()
        message = f"Joke: {joke}\nAdvice: {advice}"
        send_message(message, phone_number)
        return redirect(url_for("success"))
    return render_template("index.html")
```

The web form submits a phone number, then `send_message()` texts a random joke and a piece of advice to that number.
