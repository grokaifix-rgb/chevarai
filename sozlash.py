# -*- coding: utf-8 -*-
"""
Chevar AI — sozlash yordamchisi.
Terminalda savol-javob orqali config.json ni to'ldiradi.
Ishga tushirish:  SOZLASH.command faylini ikki marta bosing.
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
FAYL = os.path.join(BASE, "config.json")


def yukla():
    try:
        with open(FAYL, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def sora(savol, hozirgi, izoh=""):
    if izoh:
        print("   " + izoh)
    korsat = str(hozirgi) if hozirgi not in ("", None) else "bo'sh"
    javob = input(savol + "\n   [hozirgi: " + korsat + "] > ").strip()
    return javob if javob else hozirgi


def main():
    cfg = yukla()
    print("=" * 60)
    print("             CHEVAR AI — SOZLASH")
    print("=" * 60)
    print("Har bir savolga javob yozing. O'zgartirmoqchi bo'lmasangiz — Enter bosing.\n")

    cfg["bot_token"] = sora(
        "1) Bot tokeni:", cfg.get("bot_token", ""),
        "Telegramda @BotFather -> /newbot -> bot nomini bering -> token oling")

    print()
    hozirgi = ",".join(str(x) for x in (cfg.get("admin_ids") or
                                        ([cfg["admin_id"]] if cfg.get("admin_id") else [])))
    xom = sora(
        "2) Admin ID raqamlari (vergul bilan, bir nechta bo'lishi mumkin):", hozirgi,
        "Telegramda @userinfobot ga /start yozing — ID sizga chiqadi")
    cfg["admin_ids"] = [int(x) for x in str(xom).replace(" ", "").split(",")
                        if x.strip().isdigit()]
    cfg.pop("admin_id", None)

    print()
    cfg["komissiya_foiz"] = sora(
        "3) Platforma komissiyasi (foizda):", cfg.get("komissiya_foiz", 35),
        "Umumiy narxdan sizga qoladigan ulush. Tavsiya: 30-40")
    cfg["oldindan_tolov_foiz"] = sora(
        "4) Oldindan to'lov (foizda):", cfg.get("oldindan_tolov_foiz", 50),
        "Ish boshlanishidan oldin olinadigan qism. Tavsiya: 50")
    try:
        cfg["komissiya_foiz"] = float(cfg["komissiya_foiz"])
        cfg["oldindan_tolov_foiz"] = float(cfg["oldindan_tolov_foiz"])
    except Exception:
        pass

    print()
    cfg["yetkazish_narx"] = sora(
        "5) Yetkazib berish narxi (so'mda):", cfg.get("yetkazish_narx", 25000))
    cfg["bepul_yetkazish_chegara"] = sora(
        "6) Qaysi summadan yuqorida yetkazish bepul:",
        cfg.get("bepul_yetkazish_chegara", 500000))
    try:
        cfg["yetkazish_narx"] = int(float(cfg["yetkazish_narx"]))
        cfg["bepul_yetkazish_chegara"] = int(float(cfg["bepul_yetkazish_chegara"]))
    except Exception:
        pass

    print()
    cfg["karta_raqam"] = sora("7) To'lov uchun karta raqami:", cfg.get("karta_raqam", ""))
    cfg["karta_egasi"] = sora("8) Karta egasining ismi:", cfg.get("karta_egasi", ""))
    cfg["aloqa_telefon"] = sora("9) Aloqa telefoni:", cfg.get("aloqa_telefon", ""))
    cfg["aloqa_telegram"] = sora("10) Aloqa uchun Telegram username:", cfg.get("aloqa_telegram", ""))

    print("\n" + "-" * 60)
    print("AI (sun'iy intellekt) sozlamasi")
    print("-" * 60)
    print("Bot AI'siz ham ishlaydi — ichki tahlil bilan savollar beradi.")
    print("Yanada aqlli suhbat uchun bepul Google Gemini kalitini ulash mumkin:")
    print("   https://aistudio.google.com/apikey  (bepul, kartasiz)\n")
    print("Variantlar: yoq / gemini / openai / claude")
    cfg["ai_provider"] = sora("11) AI turi:", cfg.get("ai_provider", "yoq")).lower()
    if cfg["ai_provider"] not in ("yoq", "", "offline"):
        cfg["ai_key"] = sora("12) AI kaliti (API key):", cfg.get("ai_key", ""))
        cfg["ai_model"] = sora("13) Model nomi (bo'sh qoldirsangiz standart):",
                               cfg.get("ai_model", ""))
    else:
        cfg["ai_provider"] = "yoq"

    cfg.setdefault("platforma_nomi", "Chevar AI")

    with open(FAYL, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("✅ Saqlandi!")
    print("Endi ISHGA-TUSHIRISH.command faylini bosib botni yoqing.")
    print("=" * 60)


if __name__ == "__main__":
    main()
