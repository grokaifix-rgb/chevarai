#!/bin/bash
cd "$(dirname "$0")"
clear
PLIST="$HOME/Library/LaunchAgents/uz.mirzabek.chevarai.plist"
launchctl unload "$PLIST" 2>/dev/null
rm -f "$PLIST"
pkill -f "$(pwd)/bot.py" 2>/dev/null
sleep 2
echo "🛑 Bot to'xtatildi."
echo ""
echo "Qayta yoqish uchun: ISHGA-TUSHIRISH.command (bir martalik)"
echo "                    AVTOMATIK-YOQISH.command (doimiy)"
echo ""
read -n 1 -s
