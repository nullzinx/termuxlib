# termuxlib 📱🐍

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/) [![Platform](https://img.shields.io/badge/platform-Android%20(Termux)-green.svg)](https://termux.dev/) [![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A lightweight, type-annotated Python wrapper around Termux API command‑line utilities on Android.

`termuxlib` exposes native `termux-api` utilities as structured static Python classes, allowing you to control hardware, sensors, notifications, SMS, text-to-speech, camera, GPS, and Wi-Fi in few lines of code.

--- 

## Table of Contents 

* [Prerequisites](#prerequisites) 
* [Installation](#installation) 
* [Core Concept](#core-concept) 
* [Quick Start](#quick-start) 
* [Features](#features) 
* [API Reference](#api-reference) 
* [Error Handling](#error-handling) 
* [Examples](#examples) 
* [Project Structure](#project-structure) 
* [Tech Stack](#tech-stack) 
* [License](#license) 
* [Contributing](#contributing) 
* [Footer](#footer)

---

## Prerequisites 

Your Android environment must have Termux and its API package configured:

1. Install the main **[Termux](https://github.com/termux/termux-app)** application.
2. Install the **[Termux:API](https://github.com/termux/termux-api)** addon.
3. Inside Termux, run:
   ```bash
   pkg update && pkg install termux-api python -y
   ```
4. Ensure the *Termux:API* app has the required Android permissions (Location, SMS, Contacts, Camera, etc.).

---

## Installation 


You can  install the package using pip
```bash
pip install termuxlib 
```

---

## Core Concept 

All wrappers are defined as `@staticmethod` functions inside organized modules. 

Complex data outputs (such as battery status, location, sensor and network lists) are returned as raw JSON strings directly from the underlying Termux CLI. This keeps the library lightweight and lets you parse outputs as needed:

```python
import json
from termuxlib import device

battery = json.loads(device.battery_status())
print(f"Battery level: {battery['percentage']}% ({battery['status']})")
```

---

## Quick Start 

```python
from termuxlib import send_notification, device, tts, clipboard

send_notification("System Alert", "Process started.")
print(device.battery_status())
tts.speak("Termux lib loaded.")
clipboard.copy("Hello from Python!")
```

---

## Features ✨

*   **Notifications:** Send native Android notifications.
*   **Device & Sensors:** Access hardware information (battery, GPS, sensors) and manage fingerprint authentication.
*   **Text-to-Speech:** Synthesize spoken text using the Android TTS engine.
*   **SMS Management:** Send SMS messages and access contact lists.
*   **Telephony:** Retrieve network information and initiate calls.
*   **Wi-Fi Control:** Get current Wi-Fi connection details and scan for networks.
*   **Clipboard Access:** Copy text to and read from the system clipboard.
*   **Camera & Flashlight:** Capture photos and control the device's torch.
*   **Lightweight Design:** Minimalistic wrapper around Termux CLI utilities.
*   **Type Hinting:** Enhanced code readability and maintainability with type annotations.

---

## API Reference 

### 1. Notifications 

#### `send_notification(title: str, content: str) -> None`
Triggers a native Android notification.
```python
from termuxlib import send_notification
send_notification("Title", "Body message")
```

---

### 2. Device & Sensors (`device`) 

Provides access to hardware information and physical sensors.

| Method | Return | Description |
| :--- | :--- | :--- |
| `battery_status()` | `str` (JSON) | Retrieves battery state (level, health, temperature). |
| `location_gps()` | `str` (JSON) | Gets GPS location (latitude, longitude, altitude). |
| `sensor_list()` | `str` (JSON) | Lists all available hardware sensors. |
| `sensor_read(target: str)` | `str` | Reads a single value from the specified sensor (e.g., `light`). |
| `get_fingerprint()` | `str` (JSON) | Prompts biometric fingerprint authentication. |

```python
from termuxlib import device

light_level = device.sensor_read("light")
print(device.get_fingerprint())
```

---

### 3. Text-to-Speech (`tts`) 

Synthesizes spoken text using the Android TTS engine.

| Method | Return | Description |
| :--- | :--- | :--- |
| `engine_list()` | `str` | Lists available TTS engines on the device. |
| `speak(text: str)` | `None` | Speaks the given text aloud. |

```python
from termuxlib import tts

print(tts.engine_list())
tts.speak("Action completed successfully.")
```

---

### 4. SMS (`sms`) 

Manages text messages and contact databases.

| Method | Return | Description |
| :--- | :--- | :--- |
| `contact_list()` | `str` (JSON) | Lists system contacts. |
| `send(phone_number: str, msg: str)` | `None` | Sends an SMS message to a phone number. |
| `sms_list()` | `str` (JSON) | Retrieves received SMS messages. |

```python
from termuxlib import sms

sms.send("+1234567890", "Automated system update.")
```

---

### 5. Telephony (`telephony`) 

Accesses cellular connection details and handles outbound calls.

| Method | Return | Description |
| :--- | :--- | :--- |
| `info()` | `str` (JSON) | Retrieves network and carrier information. |
| `makecall(phone_number: str)` | `None` | Places an outbound call to the target number. |

```python
from termuxlib import telephony

print(telephony.info())
telephony.makecall("+1234567890")
```

---

### 6. Wi-Fi (`wifi`) 

Monitors current network states and scans nearby networks.

| Method | Return | Description |
| :--- | :--- | :--- |
| `info()` | `str` (JSON) | Retrieves details of the active Wi-Fi connection. |
| `scan_networks()` | `str` (JSON) | Performs a scan and returns visible Wi-Fi networks. |

```python
from termuxlib import wifi

print(wifi.info())
```

---

### 7. Clipboard (`clipboard`) 

Manipulates the Android system clipboard.

| Method | Return | Description |
| :--- | :--- | :--- |
| `copy(text: str)` | `None` | Copies text into the clipboard. |
| `read_clipboard()` | `str` | Reads current clipboard content. |

```python
from termuxlib import clipboard

clipboard.copy("Target payload")
print(clipboard.read_clipboard())
```

---

### 8. Camera & Flashlight (`camera`) 

Manages photo capture and toggles the hardware torch.

| Method | Return | Description |
| :--- | :--- | :--- |
| `info()` | `str` (JSON) | Retrieves device camera specifications. |
| `take_photo(output_file: str, camera: str)` | `None` | Captures a photo with the `"front"` or `"back"` camera. |
| `torch(state: bool)` | `None` | Sets the flashlight state (`True` for on, `False` for off). |

```python
from termuxlib import camera

camera.torch(True)
camera.take_photo("/sdcard/Pictures/capture.jpg", camera="back")
camera.torch(False)
```

---

## Error Handling 

All standard execution errors from Termux calls propagate as standard `subprocess.CalledProcessError`.

```python
import subprocess
from termuxlib import camera

try:
    camera.take_photo("/sdcard/image.jpg", camera="back")
except subprocess.CalledProcessError as e:
    print(f"Termux command failed: {e}")
```

---

## Examples 

To view end-to-end operational automation scripts (such as a battery alert, SMS responder, or a GPS locator):

👉 **[Go to Examples Documentation (docs/EXAMPLES.md)](docs/EXAMPLES.md)**

---

## Project Structure 

```
termuxlib/
├── src/termuxlib/
│   ├── __init__.py
│   └── main.py
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Tech Stack 

*   **Language:** Python
*   **Environment:** Android (Termux)
*   **Build System:** Setuptools

---

## License 

This project is licensed under the terms of the GNU General Public License v3.0 (GPL-3.0). See the LICENSE file for details.

---

## Contributing 

Contributions are welcome! Please feel free to submit pull requests or open issues on the GitHub repository.

---

## Footer 

© 2023 termuxlib. All rights reserved.

*   Repository: [termuxlib](https://github.com/nullzinx/termuxlib)
*   Author: nullzinx
*   Contact: [nullzinx@example.com](mailto:nullzinx@example.com) (example email)

**Give a 🌟 if you like this project!**



---
**<p align="center">Generated by [ReadmeCodeGen](https://www.readmecodegen.com/)</p>**
