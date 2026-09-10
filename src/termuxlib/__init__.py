'''termuxlib
A lightweight Python wrapper around Termux command‑line utilities.

This module provides a collection of static helper classes that invoke the
corresponding ``termux-*`` commands via :pyfunc:`subprocess.run` and return the
decoded output.  The functions are deliberately simple – they do not attempt to
parse the JSON output; callers can ``json.loads`` the result if desired.

All public methods are defined as ``@staticmethod`` so they can be accessed as
``device.battery_status()`` etc.  Errors from the subprocess are raised as
``subprocess.CalledProcessError`` because ``check=True`` is used where
appropriate.
''' 

import subprocess
from typing import Any


def send_notification(title: str, content: str) -> None:
    """Send a Termux notification.

    Parameters
    ----------
    title:
        Notification title.
    content:
        Notification body.
    """
    subprocess.run(
        [
            "termux-notification",
            "-t",
            title,
            "-c",
            content,
        ],
        check=True,
    )


class device:
    """Utility wrapper for various ``termux-`` device commands."""

    @staticmethod
    def battery_status() -> str:
        """Return raw JSON string with battery information."""
        return subprocess.run(
            "termux-battery-status",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()

    @staticmethod
    def location_gps() -> str:
        """Return raw JSON string with GPS location data."""
        return subprocess.run(
            "termux-location -p gps",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()

    @staticmethod
    def sensor_list() -> str:
        """Return raw JSON string listing available sensors."""
        return subprocess.run(
            "termux-sensor -l",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()

    @staticmethod
    def sensor_read(target: str) -> str:
        """Read a single value from *target* sensor.

        Parameters
        ----------
        target:
            Sensor name as accepted by ``termux-sensor -s``.
        """
        return subprocess.run(
            ["termux-sensor", "-s", target, "-n", "1"],
            capture_output=True,
            check=True,
        ).stdout.decode()

    @staticmethod
    def get_fingerprint() -> str:
        """Return raw JSON string with fingerprint authentication result."""
        return subprocess.run(
            "termux-fingerprint",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()


class tts:
    """Text‑to‑speech helpers."""

    @staticmethod
    def engine_list() -> str:
        """Return a newline‑separated list of available TTS engines."""
        return subprocess.run(
            "termux-tts-engines",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()

    @staticmethod
    def speak(text: str) -> None:
        """Speak *text* using the default TTS engine."""
        subprocess.run(["termux-tts-speak", text], check=True)


class sms:
    """SMS related utilities."""

    @staticmethod
    def contact_list() -> str:
        """Return raw JSON string with contact information."""
        return subprocess.run(
            "termux-contact-list",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()

    @staticmethod
    def send(phone_number: str, msg: str) -> None:
        """Send an SMS message.

        Parameters
        ----------
        phone_number:
            Destination number.
        msg:
            Message body.
        """
        subprocess.run(
            ["termux-sms-send", "-n", phone_number, msg],
            check=True,
        )

    @staticmethod
    def sms_list() -> str:
        """Return raw JSON string with received SMS messages."""
        return subprocess.run(
            "termux-sms-list",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()


class telephony:
    """Telephony helpers."""

    @staticmethod
    def info() -> str:
        """Return raw JSON string with device telephony info."""
        return subprocess.run(
            "termux-telephony-deviceinfo",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()

    @staticmethod
    def makecall(phone_number: str) -> None:
        """Initiate a phone call to *phone_number*.
        """
        subprocess.run(["termux-telephony-call", phone_number], check=True)


class wifi:
    """Wi‑Fi related helpers."""

    @staticmethod
    def info() -> str:
        """Return raw JSON string with current Wi‑Fi connection info."""
        return subprocess.run(
            "termux-wifi-connectioninfo",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()

    @staticmethod
    def scan_networks() -> str:
        """Return raw JSON string with scanned Wi‑Fi networks."""
        return subprocess.run(
            "termux-wifi-scaninfo",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()


class clipboard:
    """Clipboard helpers."""

    @staticmethod
    def copy(text: str) -> None:
        """Copy *text* to the system clipboard."""
        subprocess.run(["termux-clipboard-set", text], check=True)

    @staticmethod
    def read_clipboard() -> str:
        """Return the current clipboard contents as a string."""
        return subprocess.run(
            "termux-clipboard-get",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()


class camera:
    """Camera utilities for taking photos and controlling the torch."""

    @staticmethod
    def info() -> str:
        """Return raw JSON string with camera capabilities."""
        return subprocess.run(
            "termux-camera-info",
            shell=True,
            capture_output=True,
            check=True,
        ).stdout.decode()

    @staticmethod
    def take_photo(output_file: str, camera: str = "back") -> None:
        """Capture a photo.

        Parameters
        ----------
        output_file:
            Destination filename (e.g. ``/sdcard/photo.jpg``).
        camera:
            Either ``"front"`` or ``"back"``.  Defaults to back camera.
        """
        camera_index = "0" if camera == "front" else "1"
        subprocess.run(
            ["termux-camera-photo", "-c", camera_index, output_file],
            check=True,
        )

    @staticmethod
    def torch(state: bool) -> None:
        """Turn the device torch on or off.

        Parameters
        ----------
        state:
            ``True`` to turn on, ``False`` to turn off.
        """
        cmd = "termux-torch on" if state else "termux-torch off"
        subprocess.run(cmd, shell=True, check=True)


__all__ = [
    "send_notification",
    "device",
    "tts",
    "sms",
    "telephony",
    "wifi",
    "clipboard",
    "camera",
]
