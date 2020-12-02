import os
from datetime import date, datetime, timedelta
from adhan import adhan
from adhan.methods import ISNA, ASR_STANDARD

# Calculation Config
LAT = float(os.getenv("LAT", "0.0"))
LON = float(os.getenv("LON", "0.0"))

FAJR_ANGLE = float(os.getenv("FAJR_ANGLE", str(ISNA["fajr_angle"])))
ISHA_ANGLE = float(os.getenv("ISHA_ANGLE", str(ISNA["isha_angle"])))

ZUHR_OFFSET = int(os.getenv("ZUHR_OFFSET", 0))
MAGRHIB_OFFSET = int(os.getenv("MAGRHIB_OFFSET", 0))
ISHA_AFTER_MAGHRIB_OFFSET = (
    int(os.getenv("ISHA_AFTER_MAGHRIB_OFFSET"))
    if os.getenv("ISHA_AFTER_MAGHRIB_OFFSET")
    else None
)

params = {}
params.update({"fajr_angle": FAJR_ANGLE, "isha_angle": ISHA_ANGLE})
params.update(ASR_STANDARD)


def get_adhans_for_day(day):
    adhan_dict = adhan(
        day=day,
        location=(LAT, LON),
        parameters=params,
    )
    if ISHA_AFTER_MAGHRIB_OFFSET:
        adhan_dict["isha"] = adhan_dict["maghrib"] + timedelta(
            minutes=ISHA_AFTER_MAGHRIB_OFFSET
        )
    if ZUHR_OFFSET:
        adhan_dict["zuhr"] = adhan_dict["zuhr"] + +timedelta(minutes=ZUHR_OFFSET)
    if MAGRHIB_OFFSET:
        adhan_dict["maghrib"] = adhan_dict["maghrib"] + +timedelta(
            minutes=MAGRHIB_OFFSET
        )
    return sorted([(k, v) for k, v in adhan_dict.items()], key=lambda x: x[1])


def get_adhans():
    adhan_list = []
    adhan_list.extend(get_adhans_for_day(date.today() - timedelta(days=1)))
    adhan_list.extend(get_adhans_for_day(date.today()))
    adhan_list.extend(get_adhans_for_day(date.today() + timedelta(days=1)))

    now = datetime.now()

    next_adhan = None
    adhans = []
    for index, adhan in enumerate(adhan_list):
        name, time = adhan
        if name == "shuruq":
            continue
        day = time.strftime("%a")
        adhan = {
            "name": name,
            "isodate": time.isoformat(),
            "time": time.strftime("%a %H:%M"),
            "future": False,
            "next": False,
            "datetime": time,
        }
        if time >= now:
            adhan["future"] = True
            if not next_adhan:
                next_adhan = index
                adhan["next"] = True

        adhans.append(adhan)

    adhans = adhans[next_adhan - 2 : next_adhan + 3]

    return adhans


def get_next_adhan():
    now = datetime.now()
    adhans = get_adhans()
    for adhan in adhans:
        if adhan["next"]:
            return adhan
    return None