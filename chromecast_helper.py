import os
import pychromecast
from time import sleep

VOLUME = float(os.getenv("VOLUME", "0.34"))
MEDIA_TYPE = os.getenv("MEDIA_TYPE", "audio/mp3")
CAST_DEVICE_NAME = os.getenv("CAST_DEVICE_NAME", "My device")


def get_cast():
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=[CAST_DEVICE_NAME]
    )
    pychromecast.discovery.stop_discovery(browser)

    if not len(chromecasts):
        print("No chromecast")
        return None

    cast = chromecasts[0]
    cast.wait()
    return cast


def stop_app():
    cast = get_cast()
    if not cast:
        return
    cast.quit_app()
    cast.wait()


def status():
    cast = get_cast()
    if not cast:
        return {"found_cast": False}

    return {
        "found_cast": True,
        "is_idle": cast.is_idle,
        "display_name": cast.status.display_name,
        "status_text": cast.status.status_text,
        "volume": int(VOLUME * 100),
    }


def volume(level):
    global VOLUME
    VOLUME = level
    cast = get_cast()
    if not cast:
        return
    cast.set_volume(VOLUME)
    cast.wait()


def play(url, title=None):
    global VOLUME
    cast = get_cast()
    if not cast:
        return

    is_idle = cast.is_idle

    if not is_idle:
        print("Not idle")
        return

    print("Playing " + url)
    cast.set_volume(VOLUME)
    mc = cast.media_controller
    mc.play_media(url, MEDIA_TYPE, title=title)
    mc.block_until_active()
