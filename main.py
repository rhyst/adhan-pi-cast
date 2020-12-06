import os
from datetime import date, datetime, timedelta
from time import sleep
from multiprocessing import Process
from flask import Flask, request, render_template, redirect, url_for, jsonify
import schedule

from adhan_helper import get_adhans, get_next_adhan
from chromecast_helper import play, status, stop_app, volume

# Flask Config
PORT = os.getenv("PORT", "5000")
HOST = os.getenv("HOST", "0.0.0.0")

# Adhan Media Config
FAJR_MEDIA_URL = os.getenv("FAJR_MEDIA_URL", "{}:{}/static/fajr.mp3".format(HOST, PORT))
ZUHR_MEDIA_URL = os.getenv("ZUHR_MEDIA_URL", "{}:{}/static/zuhr.mp3".format(HOST, PORT))
ASR_MEDIA_URL = os.getenv("ASR_MEDIA_URL", "{}:{}/static/asr.mp3".format(HOST, PORT))
MAGHRIB_MEDIA_URL = os.getenv(
    "MAGHRIB_MEDIA_URL", "{}:{}/static/maghrib.mp3".format(HOST, PORT)
)
ISHA_MEDIA_URL = os.getenv("ISHA_MEDIA_URL", "{}:{}/static/isha.mp3".format(HOST, PORT))

# Run config
IS_ON = os.getenv("IS_ON", "0")

app = Flask(__name__)

is_on = IS_ON != "0"

def get_title(adhan):
    return "Prayer for " + adhan.title()


def get_url_for_adhan(adhan):
    return {
        "fajr": FAJR_MEDIA_URL,
        "zuhr": ZUHR_MEDIA_URL,
        "asr": ASR_MEDIA_URL,
        "maghrib": MAGHRIB_MEDIA_URL,
        "isha": ISHA_MEDIA_URL,
    }[adhan.lower()]


def play_adhan(adhan):
    print("Playing {}".format(adhan["name"]))
    # Play Adhan
    play(get_url_for_adhan(adhan["name"]), title=get_title(adhan["name"]))
    # Schedule next Adhan
    next_adhan = get_next_adhan()
    schedule.every().day.at(next_adhan["datetime"].strftime("%H:%M:%S")).do(
        play_adhan, next_adhan
    )


def scheduling():
    next_adhan = get_next_adhan()
    schedule.every().day.at(next_adhan["datetime"].strftime("%H:%M:%S")).do(
        play_adhan, next_adhan
    )
    while 1:
        schedule.run_pending()
        print("scheduling")
        sleep(1)


@app.route("/", methods=["POST", "GET"])
def index():
    global is_on
    return render_template(
        "index.html", adhans=get_adhans(), is_on=is_on, status=status()
    )


scheduling_process = None
if is_on:
    scheduling_process = Process(target=scheduling)
    scheduling_process.start()

@app.route("/toggle", methods=["POST"])
def toggle():
    global is_on
    global scheduling_process
    is_on = False if is_on else True
    if is_on:
        scheduling_process = Process(target=scheduling)
        scheduling_process.start()
    else:
        scheduling_process.kill()
    return redirect("/")


@app.route("/stop", methods=["POST"])
def stop():
    stop_app()
    return redirect("/")


@app.route("/play", methods=["POST"])
def force_play():
    stop_app()
    adhan = request.form.get("adhan")
    url = get_url_for_adhan(adhan)
    play(url, title=get_title(adhan))
    return redirect("/")


@app.route("/volume", methods=["POST"])
def set_volume():
    volume(request.json["volume"])
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
