## Pushover support version has here
https://github.com/yueplush/vrchat-join-notification-with-pushover

# VRChat Join Notification (Linux)

A simple log-watcher that notifies you when someone joins your current VRChat world.  
No unofficial API calls – it only reads your **local VRChat logs** (safe and ToS-friendly).

![screenshot](https://raw.githubusercontent.com/yueplush/vrchat-join-notification/refs/heads/main/notify.png)  
*(example notification on GNOME desktop)*

---

# Features
- ToS-safe: no API keys, only local logs
- Desktop notification via `notify-send`
- Auto-switches to the latest VRChat log after restart
- Optional: custom icon or sound
- Quick installer (`install.sh`) with distro detection (Debian/Ubuntu, Fedora/Bazzite, Arch/Manjaro)

## Specified behavior
The popup will still appear when you join the world, so please be patient.

---
## depency
flatpak version steam recommend
python 3.13 or higher

---

# Install

```bash
git clone https://github.com/yueplush/vrchat-join-notification.git
cd vrchat-join-notification
chmod +x install.sh
bash ./install.sh
```

This will:
Install dependencies (libnotify) if supported
Copy the script to ~/.local/bin/vrc_join_notify.py
Register and start the systemd user service vrc-join-notify.service

# uninstall

```bash
cd vrchat-join-notification
chmod +x uninsatll.sh
bash ./uninstall.sh
```

# if you want change something notification style
Open the top of vrc_join_notify.py and edit:

```bash
TITLE = "VRChat"
ICON = "/path/to/icon.png"   # Optional
SOUND = "/usr/share/sounds/freedesktop/stereo/message.oga"  # Optional
```
Change ICON to use a custom PNG in notifications
Change SOUND to play a sound using paplay

License
MIT




