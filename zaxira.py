# -*- coding: utf-8 -*-
"""
Chevar AI — ma'lumotlar bazasini zaxiralash va tiklash (server hisobidan mustaqil).

  /zaxira   — admin bazaning to'liq nusxasini (data.json) Telegramda fayl sifatida oladi
  avtomatik — har kuni bir marta bosh adminga zaxira fayl yuboriladi
  /tiklash  — admin zaxira faylni yuboradi, bot tasdiqdan so'ng bazani shu fayl bilan almashtiradi

Bu boshqa serverga yoki Railway hisobiga ko'chishda bazani yo'qotmaslik uchun.

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

import json
import os
import ssl
import time
import urllib.request
import uuid

import core
from core import (ADMINLAR, API, BOSH_ADMIN, DATA, DATA_FILE, SSL_CTX, TOKEN, api, holat,
                  holat_ol, holat_tozala, log, saqla, tugmalar, vaqt, yubor)

_KUNLIK_SOAT = 3  # Toshkent vaqti ~08:00 (server UTC)


def _hujjat_yubor(chat_id, nom, mazmun, izoh=""):
    chegara = uuid.uuid4().hex
    qism = []
    for k, v in (("chat_id", str(chat_id)), ("caption", izoh), ("parse_mode", "HTML")):
        qism.append(("--" + chegara + "\r\nContent-Disposition: form-data; name=\"" + k
                     + "\"\r\n\r\n" + v + "\r\n").encode("utf-8"))
    qism.append(("--" + chegara + "\r\nContent-Disposition: form-data; name=\"document\"; filename=\""
                 + nom + "\"\r\nContent-Type: application/json\r\n\r\n").encode("utf-8") + mazmun
                + ("\r\n--" + chegara + "--\r\n").encode("utf-8"))
    req = urllib.request.Request(API.format(token=TOKEN, method="sendDocument"), data=b"".join(qism),
                                 headers={"Content-Type": "multipart/form-data; boundary=" + chegara})
    with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
        return json.loads(r.read().decode("utf-8"))


def _hajm_matni():
    return (str(len(DATA.get("foydalanuvchilar", {}))) + " foydalanuvchi, "
            + str(len(DATA.get("buyurtmalar", {}))) + " tikish buyurtmasi, "
            + str(len(DATA.get("sotuvlar", {}))) + " do'kon buyurtmasi, "
            + str(len(DATA.get("mahsulotlar", {}))) + " mahsulot, "
            + str(len(DATA.get("dizaynlar", {}))) + " dizayn")


def zaxira_yubor(chat_id, sabab="so'rov"):
    saqla()
    with open(DATA_FILE, "rb") as f:
        mazmun = f.read()
    nom = "chevar_zaxira_" + time.strftime("%Y-%m-%d_%H-%M") + ".json"
    try:
        j = _hujjat_yubor(chat_id, nom, mazmun,
                          "💾 <b>Baza zaxirasi</b> (" + sabab + ")\n" + _hajm_matni()
                          + "\n\n<i>Saqlab qo'ying. Tiklash: /tiklash</i>")
        fid = j.get("result", {}).get("document", {}).get("file_id", "")
        log("Zaxira yuborildi: " + nom + " · " + _hajm_matni() + " · file_id=" + fid)
        return True
    except Exception as e:
        log("Zaxira yuborilmadi: " + str(e))
        yubor(chat_id, "❗️ Zaxirani yuborib bo'lmadi: " + str(e)[:200])
        return False


def kunlik_tekshir():
    """Asosiy sikldan chaqiriladi: kuniga bir marta bosh adminga zaxira."""
    bugun = time.strftime("%Y-%m-%d")
    if DATA.get("oxirgi_zaxira") == bugun or time.gmtime().tm_hour < _KUNLIK_SOAT:
        return
    if BOSH_ADMIN and zaxira_yubor(BOSH_ADMIN, "kunlik avtomatik"):
        DATA["oxirgi_zaxira"] = bugun
        saqla()


# =====================  Tiklash  =====================

def tiklash_boshla(uid):
    holat(uid, "tiklash")
    saqla()
    yubor(uid, "♻️ <b>Bazani tiklash</b>\n\nZaxira faylini (chevar_zaxira_….json) shu yerga yuboring.\n"
               "⚠️ Hozirgi baza shu fayl bilan <b>almashtiriladi</b>. Bekor qilish: /bekor")


def fayl_qabul(uid, msg):
    doc = msg.get("document") or {}
    if not doc.get("file_name", "").endswith(".json"):
        yubor(uid, "Bu .json zaxira fayli emas.")
        return
    r = api("getFile", file_id=doc["file_id"])
    if not r or not r.get("ok"):
        yubor(uid, "Faylni olib bo'lmadi.")
        return
    url = "https://api.telegram.org/file/bot" + TOKEN + "/" + r["result"]["file_path"]
    with urllib.request.urlopen(url, timeout=120, context=SSL_CTX) as f:
        mazmun = f.read()
    try:
        yangi = json.loads(mazmun.decode("utf-8"))
        assert isinstance(yangi.get("foydalanuvchilar"), dict)
    except Exception:
        yubor(uid, "❗️ Fayl buzilgan yoki Chevar AI zaxirasi emas.")
        return
    tmp = DATA_FILE + ".tiklash"
    with open(tmp, "wb") as f:
        f.write(mazmun)
    holat(uid, "tiklash_tasdiq")
    saqla()
    yubor(uid, "📄 Faylda: " + str(len(yangi.get("foydalanuvchilar", {}))) + " foydalanuvchi, "
          + str(len(yangi.get("buyurtmalar", {}))) + " buyurtma, "
          + str(len(yangi.get("sotuvlar", {}))) + " do'kon buyurtmasi.\n"
          "Hozirgi bazada: " + _hajm_matni() + ".\n\nAlmashtiraymi?",
          kb=tugmalar([[("✅ Ha, tiklash", "tik_ha"), ("❌ Yo'q", "tik_yoq")]]))


def tiklash_tasdiq(uid, ha):
    tmp = DATA_FILE + ".tiklash"
    holat_tozala(uid)
    if not ha or not os.path.exists(tmp):
        if os.path.exists(tmp):
            os.remove(tmp)
        saqla()
        yubor(uid, "Tiklash bekor qilindi.")
        return
    # Avval hozirgi bazani ham zaxiralab qo'yamiz
    zaxira_yubor(uid, "tiklashdan oldingi holat")
    with open(tmp, encoding="utf-8") as f:
        yangi = json.load(f)
    offset = DATA.get("offset", 0)
    media = DATA.get("media", {})
    DATA.clear()
    DATA.update(yangi)
    DATA["offset"] = max(offset, DATA.get("offset", 0))  # eski xabarlar qayta ishlanmasin
    DATA.setdefault("media", {}).update({k: v for k, v in media.items() if k not in DATA["media"]})
    for k, v in (("keyingi_raqam", 1001), ("foydalanuvchilar", {}), ("holatlar", {}),
                 ("buyurtmalar", {}), ("dizaynlar", {}), ("mahsulotlar", {}), ("savatlar", {}),
                 ("sotuvlar", {}), ("keyingi_sotuv", 5001), ("keyingi_dizayn", 1),
                 ("keyingi_mahsulot", 1)):
        DATA.setdefault(k, v)
    saqla()
    os.remove(tmp)
    log("Baza tiklandi: " + _hajm_matni())
    yubor(uid, "✅ <b>Baza tiklandi.</b>\n" + _hajm_matni())
