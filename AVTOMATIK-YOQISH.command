#!/bin/bash
cd "$(dirname "$0")"
clear
PAPKA="$(pwd)"
PLIST="$HOME/Library/LaunchAgents/uz.mirzabek.chevarai.plist"
LOG="$HOME/Library/Logs/chevarai.log"
PY="$(command -v python3)"
mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"

# Diqqat: jurnal fayli Desktop ichida BO'LMASLIGI kerak —
# macOS launchd'ga u papkaga yozishga ruxsat bermaydi (xato 78).
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>uz.mirzabek.chevarai</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PY</string>
    <string>-u</string>
    <string>$PAPKA/bot.py</string>
  </array>
  <key>WorkingDirectory</key><string>$PAPKA</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
PL

launchctl unload "$PLIST" 2>/dev/null
launchctl load "$PLIST"
sleep 5

if pgrep -f "$PAPKA/bot.py" > /dev/null; then
  echo "✅ Bot doimiy ishlaydigan qilib qo'yildi."
  echo "   Kompyuter yoqilganda o'zi ishga tushadi."
else
  echo "⚠️ Bot ishga tushmadi. Jurnalni ko'ring:"
  echo "   $LOG"
fi
echo ""
echo "Jurnal: $LOG"
echo "To'xtatish uchun: TOXTATISH.command"
echo ""
read -n 1 -s
