# Adhan Pi Cast

Do you have:

- A Google Cast Device?
- A Raspberry Pi or other always on computer in your house?
- A desire to hear the Adhan prayers at the appropriate times over your cast device?

Then this is the script for you.

## Configuration

You can set the following environment variables:

- `CAST_DEVICE_NAME` The friendly name of the device or group to cast to.
- `HOST` The host name for the server. If using with docker/docker-compose then this should be left as the default. Default `0.0.0.0`.
- `PORT` The port for the server. The docker container must be run with `network-mode: host` so this is the port on the host, even in a docker container (i.e. port mapping will not work). Default `5000`.
- `MEDIA_TYPE` The media content type for the prayer media. Default `audio/mp3`.
- `LAT` Your latitude for determination of prayer times. Default `0.0`
- `LON` Your longitude for determination of prayer times. Default `0.0`
- `FAJR_ANGLE` The fajr angle to use when determining prayer times. Defaults to ISNA configuration.
- `ISHA_ANGLE` The isha angle to use when determining prayer times. Defaults to ISNA configuration.
- `ISHA_AFTER_MAGHRIB_OFFSET` Use time offset from Maghrib rather than angle for determining isha prayer time. Default not set.
- `MAGRHIB_OFFSET` Time offset for Maghrib. Default `0`.
- `ZUHR_OFFSET` Time offset for Zuhr. Default `0`

The following urls must be accessible to the cast device.

- `FAJR_MEDIA_URL` The url for the fajr prayer.
- `ZUHR_MEDIA_URL` The url for the zuhr prayer.
- `ASR_MEDIA_URL` The url for the asr prayer.
- `MAGHRIB_MEDIA_URL` The url for the maghrib prayer.
- `ISHA_MEDIA_URL` The url for the isha prayer.

One way to set this up is to place your prayer audio files in the `static` directory and then set the `*_MEDIA_URL` variables to include to include the publically accessible IP address or URL of the server. For example if your server is available on your local network at `192.168.0.10` and you have saved the media as `fajr.mp3` in the `static` directory then you might set the url for the fajr prayer (`FAJR_MEDIA_URL`) to `http://192.168.0.10/static/fajr.mp3`.

Alternatively if you have access to media on the internet then you can just set the media urls accordingly i.e. you might set `FAJR_MEDIA_URL` to `https://some.website.com/a/path/fajr.mp3`.

These can be set as environment variables on your system, in the docker run command, or in the docker compose config file.

## Run

### Docker

Build the docker image and run the container:

```
docker build -t adhan-pi-cast .;
docker run --rm -p 5000:5000 adhan-pi-cast;
```

### Docker-compose

Modify and use the provided `docker-compose.yml` config file.

### Non-docker

Modify the `run` script environment variables and then run it:

```
./run
```

## Usage

Access the UI by navigating a browser at the host using the port you specified (i.e. `http://192.168.0.1:5000`). Features:

- Turn the scheduled Adhans on and off
- Immediately play an Adhan
- Set the volume Adhans should play at
- See cast device status
- Stop current cast app

By default the scheduled Adhans are off and they will only play if the cast device is idle.
