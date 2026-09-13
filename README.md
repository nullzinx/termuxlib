# termuxlib

A Python library for interacting with Android devices through **Termux:API**.

`termuxlib` provides a Python interface over Termux:API commands, allowing Python programs to access Android features such as notifications, battery information, GPS, sensors, text-to-speech, SMS, telephony, Wi-Fi, clipboard, camera, and flashlight control.

> **Status:** Work in progress.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [How It Works](#how-it-works)
- [API Reference](#api-reference)
  - [`notification`](#notification)
  - [`device`](#device)
  - [`tts`](#tts)
  - [`sms`](#sms)
  - [`telephony`](#telephony)
  - [`wifi`](#wifi)
  - [`clipboard`](#clipboard)
  - [`camera`](#camera)
- [Return Values](#return-values)
- [Permissions](#permissions)
- [Dependencies](#dependencies)
- [Examples](#examples)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

# Requirements

`termuxlib` requires an Android device running Termux and Termux:API.

### Required software

- Android
- Termux
- Termux:API Android application
- Python
- `termux-api` Termux package

Install the Termux package with:

```bash
pkg install termux-api
```

The **Termux:API Android application** must also be installed.

Test the installation with:

```bash
termux-battery-status
```

If everything is configured correctly, the command should return battery information in JSON format.

---

# Installation

## PyPI

If `termuxlib` is published on PyPI:

```bash
pip install termuxlib
```

Then:

```python
import termuxlib
```

## From source

Clone the repository:

```bash
git clone https://github.com/nullzinx/termuxlib.git
cd termuxlib
```

Install it locally:

```bash
pip install .
```

---

# How It Works

`termuxlib` acts as a Python wrapper around Termux:API commands.

For example, the following command:

```bash
termux-battery-status
```

can be exposed through Python as:

```python
device.battery_status()
```

Internally, the library uses Python's `subprocess` module to execute Termux commands.

JSON output produced by Termux:API is converted into Python data structures.

```text
Python application
       │
       ▼
   termuxlib
       │
       ▼
   subprocess
       │
       ▼
   Termux:API
       │
       ▼
    Android
```

---

# API Reference

## `notification`

Provides functions for interacting with Android notifications.

### `notification.send(title, content, priority, id)`

Sends a notification.

| Parameter | Type | Description |
|---|---|---|
| `title` | `str` | Notification title |
| `content` | `str` | Notification content |
| `priority` | `str` | Notification priority |
| `id` | `str` | Notification identifier |

Example:

```python
notification.send(
    "termuxlib",
    "Hello from Python",
    "high",
    "1"
)
```

Uses:

```bash
termux-notification
```

### `notification.remove(id)`

Removes a notification.

| Parameter | Type | Description |
|---|---|---|
| `id` | `str` | Notification identifier |

Example:

```python
notification.remove("1")
```

Uses:

```bash
termux-notification-remove
```

---

# `device`

Provides access to device-related Termux:API functionality.

## `device.battery_status()`

Retrieves battery information.

Uses:

```bash
termux-battery-status
```

Example:

```python
status = device.battery_status()
print(status)
```

A typical response may contain fields such as:

```json
{
    "percentage": 75,
    "plugged": "UNPLUGGED",
    "status": "DISCHARGING",
    "temperature": 31.2
}
```

The exact fields depend on the Android device and Termux:API version.

---

## `device.location_gps()`

Retrieves the device's GPS location.

Uses:

```bash
termux-location -p gps
```

Example:

```python
code, location = device.location_gps()

if code == 0:
    print(location)
```

Location access requires the appropriate Android permission.

---

## `device.sensor_list()`

Lists sensors available on the device.

Uses:

```bash
termux-sensor -l
```

Example:

```python
sensors = device.sensor_list()

if sensors == 0:
    print("Sensors retrieved successfully")
```

---

## `device.sensor_read(target)`

Reads data from a selected sensor.

| Parameter | Type | Description |
|---|---|---|
| `target` | `str` | Sensor name |

Example:

```python
code, data = device.sensor_read("accelerometer")

if code == 0:
    print(data)
```

The available sensor names depend on the device.

---

## `device.get_fingerprint()`

Requests fingerprint authentication through Termux:API.

Uses:

```bash
termux-fingerprint
```

Example:

```python
code, result = device.get_fingerprint()

if code == 0:
    print(result)
```

The result depends on the authentication state and Android device.

---

# `tts`

Provides Text-to-Speech functionality.

## `tts.engine_list()`

Lists available TTS engines.

Uses:

```bash
termux-tts-engines
```

Example:

```python
code, engines = tts.engine_list()

if code == 0:
    print(engines)
```

---

## `tts.speak(text)`

Converts text to speech.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Text to be spoken |

Example:

```python
tts.speak("Hello from Termuxlib")
```

Uses:

```bash
termux-tts-speak
```

---

# `sms`

Provides access to SMS-related Termux:API commands.

## `sms.contact_list()`

Retrieves the device's contact list.

Uses:

```bash
termux-contact-list
```

Example:

```python
code, contacts = sms.contact_list()

if code == 0:
    print(contacts)
```

Access to contacts requires Android permission.

---

## `sms.send(phone_number, msg)`

Sends an SMS message.

| Parameter | Type | Description |
|---|---|---|
| `phone_number` | `str` | Destination phone number |
| `msg` | `str` | Message content |

Example:

```python
sms.send(
    "+5511999999999",
    "Hello from termuxlib"
)
```

Uses:

```bash
termux-sms-send
```

Sending SMS requires the appropriate Android permission and a device/carrier configuration that supports SMS.

---

## `sms.sms_list()`

Retrieves SMS messages.

Uses:

```bash
termux-sms-list
```

Example:

```python
code, messages = sms.sms_list()

if code == 0:
    print(messages)
```

Reading SMS requires the appropriate Android permission.

---

# `telephony`

Provides telephony-related functionality.

## `telephony.info()`

Retrieves device telephony information.

Uses:

```bash
termux-telephony-deviceinfo
```

Example:

```python
code, information = telephony.info()

if code == 0:
    print(information)
```

The available information depends on the Android version, device, SIM configuration, and Termux:API.

---

## `telephony.makecall(phone_number)`

Initiates a phone call.

| Parameter | Type | Description |
|---|---|---|
| `phone_number` | `str` | Destination phone number |

Example:

```python
telephony.makecall("+5511999999999")
```

Uses:

```bash
termux-telephony-call
```

Phone-call functionality requires the appropriate Android permission and telephony support.

---

# `wifi`

Provides Wi-Fi information and scanning functionality.

## `wifi.info()`

Retrieves information about the current Wi-Fi connection.

Uses:

```bash
termux-wifi-connectioninfo
```

Example:

```python
code, information = wifi.info()

if code == 0:
    print(information)
```

---

## `wifi.scan_networks()`

Scans for available Wi-Fi networks.

Uses:

```bash
termux-wifi-scaninfo
```

Example:

```python
code, networks = wifi.scan_networks()

if code == 0:
    for network in networks:
        print(network)
```

Wi-Fi scanning behavior is affected by Android permissions and location-related system restrictions.

---

# `clipboard`

Provides access to the Android clipboard.

## `clipboard.copy(text)`

Copies text to the Android clipboard.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Text to copy |

Example:

```python
clipboard.copy("Hello from termuxlib")
```

Uses:

```bash
termux-clipboard-set
```

---

## `clipboard.read_clipboard()`

Reads the current clipboard contents.

Example:

```python
code, content = clipboard.read_clipboard()

if code == 0:
    print(content)
```

Uses:

```bash
termux-clipboard-get
```

---

# `camera`

Provides camera and flashlight functionality.

## `camera.info()`

Retrieves information about available cameras.

Uses:

```bash
termux-camera-info
```

Example:

```python
code, information = camera.info()

if code == 0:
    print(information)
```

---

## `camera.take_photo(outputfile, camera)`

Captures a photograph.

| Parameter | Type | Description |
|---|---|---|
| `outputfile` | `str` | Destination file path |
| `camera` | `str` | Camera to use |

Supported camera values:

- `front`
- `back`

Example:

```python
camera.take_photo(
    "/sdcard/photo.jpg",
    "back"
)
```

The underlying command is:

```bash
termux-camera-photo
```

Camera access requires the appropriate Android permission.

---

## `camera.torch(state)`

Controls the device flashlight.

| Parameter | Type | Description |
|---|---|---|
| `state` | `bool` | `True` turns the flashlight on; `False` turns it off |

Example:

```python
camera.torch(True)
```

Turn it off:

```python
camera.torch(False)
```

Uses:

```bash
termux-torch
```

---

# Return Values

Many functions return the exit status produced by the underlying Termux:API command.

Generally:

```text
0 → command succeeded
non-zero → command failed
```

Some functions return both the exit code and parsed data:

```python
code, data = device.location_gps()
```

A successful operation normally has:

```python
code == 0
```

This design allows applications to detect failures without relying exclusively on exceptions.

---

# Permissions

Termux:API operations may require Android permissions.

Depending on the functionality being used, permissions can include access to:

- Location
- Camera
- Microphone
- Contacts
- SMS
- Phone
- Sensors
- Notifications

Permissions are controlled by Android and the Termux:API application.

If an operation fails despite the command being installed, verify that the corresponding Android permission has been granted.

---

# Dependencies

The library is designed to use Python's standard library for its core implementation.

Current implementation relies primarily on:

```python
subprocess
json
random
```

The actual Android functionality is provided by Termux:API rather than by Python packages.

---

# Examples

## Battery monitor

```python
from termuxlib import device

code, battery = device.battery_status()

if code == 0:
    print(f"Battery: {battery['percentage']}%")
else:
    print("Failed to retrieve battery information")
```

---

## Notification

```python
from termuxlib import notification

notification.send(
    "System",
    "Task completed",
    "high",
    "task-1"
)
```

---

## Text-to-Speech

```python
from termuxlib import tts

tts.speak("Termuxlib is running")
```

---

## Clipboard

```python
from termuxlib import clipboard

clipboard.copy("termuxlib")

code, content = clipboard.read_clipboard()

if code == 0:
    print(content)
```

---

## Camera

```python
from termuxlib import camera

camera.take_photo(
    "/sdcard/photo.jpg",
    "back"
)
```

---

## Wi-Fi information

```python
from termuxlib import wifi

code, information = wifi.info()

if code == 0:
    print(information)
```

---

# Limitations

`termuxlib` does not directly implement Android APIs.

It depends on:

1. Termux being installed.
2. Termux:API being installed.
3. The `termux-api` package being available.
4. The required Android permissions being granted.
5. The corresponding Termux:API command being supported by the device.

Therefore, behavior can vary between Android versions and devices.

The library also inherits limitations and restrictions imposed by Android and Termux:API.

---

# Development Status

The project is currently under active development.

The API may change between versions.

Breaking changes may occur before the first stable release.

Until a stable version is released, applications using `termuxlib` should avoid assuming that the API is permanently stable.

---

# Roadmap

Potential future features include:

- [ ] Better exception handling
- [ ] Consistent return types
- [ ] Type hints throughout the API
- [ ] Automatic command availability checks
- [ ] Custom exception classes
- [ ] Improved documentation
- [ ] More Termux:API commands
- [ ] Async API
- [ ] Better subprocess management
- [ ] Unit tests
- [ ] CI/CD
- [ ] Stable PyPI releases
- [ ] API versioning

---

# Contributing

Contributions are welcome.

A typical development workflow is:

```bash
git clone https://github.com/nullzinx/termuxlib.git
cd termuxlib
```

Create a branch:

```bash
git checkout -b feature/my-feature
```

Make your changes, test them on Termux, and commit:

```bash
git add .
git commit -m "Add new feature"
```

Push the branch:

```bash
git push origin feature/my-feature
```

Then open a pull request.

When contributing, prefer small, focused changes and test functionality directly on an Android device running Termux.

---

# License

This project does not currently specify a license.

Until a license is added to the repository, the source code should not be assumed to be freely reusable, modified, or redistributed.

---

# Author

**nullzinx**

GitHub:

`https://github.com/nullzinx`

---

# Disclaimer

`termuxlib` is a wrapper around Termux:API and is not affiliated with the Termux project unless explicitly stated by the maintainers.

The functionality available through this library depends on the underlying Termux and Android environment.
