#!/bin/bash
clear
PLIST="$HOME/Library/LaunchAgents/uz.mirzabek.chevarai.plist"
launchctl unload "$PLIST" 2>/dev/null
rm -f "$PLIST"
pkill -f "python3 .*ChevarAI/bot.py" 2>/dev/null
echo "🛑 Bot to'xtatildi."
echo ""
echo "Qayta yoqish uchun: ISHGA-TUSHIRISH.command"
echo ""
read -n 1 -s
