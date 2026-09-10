#!/bin/bash
cd "$(dirname "$0")"
clear
PAPKA="$(pwd)"
PLIST="$HOME/Library/LaunchAgents/uz.mirzabek.chevarai.plist"
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>uz.mirzabek.chevarai</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/env</string>
    <string>python3</string>
    <string>$PAPKA/bot.py</string>
  </array>
  <key>WorkingDirectory</key><string>$PAPKA</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$PAPKA/bot.log</string>
  <key>StandardErrorPath</key><string>$PAPKA/bot.log</string>
</dict>
</plist>
PL
launchctl unload "$PLIST" 2>/dev/null
launchctl load "$PLIST"
echo "✅ Bot doimiy ishlaydigan qilib qo'yildi."
echo "   Kompyuter yoqilganda o'zi ishga tushadi."
echo ""
echo "To'xtatish uchun: TOXTATISH.command"
echo ""
read -n 1 -s
