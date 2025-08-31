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

# Configuration

Open the top of ~/.config/systemd/user/vrc-join-notify.service and edit:
example: sudo nano ~/.config/systemd/user/vrc-join-notify.service
then

```bash  
[Unit]
Description=VRChat Join Notifier (user)
After=default.target

[Service]
Type=simple
Environment=PUSHOVER_TOKEN=aok9oitu14k19pyynoqactfmenfh28   # Application/API Token
Environment=PUSHOVER_USER=uhbp1vszi3x8dfvxo36qrxghj2stbq   # User Key
ExecStart=%h/.local/bin/vrc_join_notify.py 
Restart=always
RestartSec=2

[Install]
WantedBy=default.target
```

token, and user key has just access to https://pushover.net/ (you can free-trial 30 day)
if dont wont proprietary here use this
https://github.com/yueplush/vrchat-join-notification

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




