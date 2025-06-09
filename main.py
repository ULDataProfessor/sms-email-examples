from flask import Flask, render_template, request, redirect, url_for
import requests
from send_sms import send_message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_joke():
    """Fetch a random joke from the API"""
    url = (
        "https://v2.jokeapi.dev/joke/Any?"
        "blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        "&type=single"
    )
    response = requests.get(url)
    data = response.json()
    return data.get("joke", "No joke available")


def get_advice():
    """Fetch random advice from the API"""
    response = requests.get("https://api.adviceslip.com/advice")
    data = response.json()
    return data["slip"]["advice"]


@app.route("/", methods=["GET", "POST"])
def index():
    """Main route that handles the form and sends messages"""
    if request.method == "POST":
        phone_number = request.form["phone_number"]
        joke = get_joke()
        advice = get_advice()
        message = f"Joke: {joke}\nAdvice: {advice}\n\n" "Brought to you by Sidney"

        # Special case for demo purposes
        special_case = "+1"  # phone number here
        if special_case == phone_number:
            send_message("This is a special message", phone_number)

        send_message(message, phone_number)
        return redirect(url_for("success"))
    return render_template("index.html")


@app.route("/success")
def success():
    """Success page after sending message"""
    success_img = (
        "https://lh3.googleusercontent.com/proxy/"
        "jYiJlLpHyue_F0I2NDK4AS7Qa8ZYHvfSMq4ZYN-eHkidKq4Pjj9FV7Td"
        "jtPlPYJSbfZ_QFJWO2QDNCbEiB6WVrFrbIHM3P7YY2bldRBSKLxu32YY"
        "D0N_mrGmFHnK33N3PWysxVjlXLtfUWsDw-AjQ0-bhKDo"
    )
    return render_template("index.html", success=True, success_img=success_img)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
