# -*- coding: utf-8 -*-
"""
Chevar AI — umumiy yadro: sozlamalar, ma'lumotlar bazasi (JSON), Telegram API.

Sozlamalar ikki joydan o'qiladi:
  1) Railway/server: muhit o'zgaruvchilari (BOT_TOKEN, ADMIN_IDS, ...)
  2) Uy kompyuteri: config.json fayli
Muhit o'zgaruvchisi ustunroq turadi.

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

import json
import os
import ssl
import threading
import time
import urllib.error
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# Railway'da Volume ulanadi: DATA_DIR=/data
DATA_DIR = os.getenv("DATA_DIR", BASE_DIR)
DATA_FILE = os.path.join(DATA_DIR, "data.json")

# Birinchi ishga tushirish: Volume hali bo'sh bo'lsa va loyihada boshlang'ich
# baza bo'lsa — uni ko'chiramiz (uy kompyuteridagi bazani serverga o'tkazish).
_BOSHLANGICH = os.path.join(BASE_DIR, "boshlangich-data.json")


def _bosh_bazami(yol):
    """Volume'dagi baza umuman bo'shmi? (fayl yo'q yoki foydalanuvchi yo'q)"""
    if not os.path.exists(yol):
        return True
    try:
        with open(yol, "r", encoding="utf-8") as f:
            d = json.load(f)
        return not d.get("foydalanuvchilar") and not d.get("buyurtmalar")
    except Exception:
        return True


if DATA_DIR != BASE_DIR and os.path.exists(_BOSHLANGICH) and _bosh_bazami(DATA_FILE):
    try:
        import shutil
        os.makedirs(DATA_DIR, exist_ok=True)
        shutil.copy(_BOSHLANGICH, DATA_FILE)
        print("Boshlang'ich baza ko'chirildi: " + DATA_FILE, flush=True)
    except Exception as _e:
        print("Boshlang'ich bazani ko'chirib bo'lmadi: " + str(_e), flush=True)

API = "https://api.telegram.org/bot{token}/{method}"


def _ssl_context():
    ctx = ssl.create_default_context()
    if ssl.get_default_verify_paths().cafile is None:
        try:
            import certifi
            ctx = ssl.create_default_context(cafile=certifi.where())
        except Exception:
            for p in ("/etc/ssl/cert.pem", "/private/etc/ssl/cert.pem",
                      "/usr/local/etc/openssl/cert.pem"):
                if os.path.exists(p):
                    ctx = ssl.create_default_context(cafile=p)
                    break
    return ctx


SSL_CTX = _ssl_context()


# =====================  Fayl bilan ishlash  =====================

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


CFG = load_json(CONFIG_FILE, {})


def sozlama(kalit, env_nomi, standart=""):
    """Avval muhit o'zgaruvchisi, keyin config.json, keyin standart qiymat."""
    qiymat = os.getenv(env_nomi)
    if qiymat not in (None, ""):
        return qiymat
    qiymat = CFG.get(kalit)
    if qiymat not in (None, ""):
        return qiymat
    return standart


def _adminlar():
    xom = os.getenv("ADMIN_IDS", "")
    royxat = [int(x) for x in xom.replace(" ", "").split(",") if x.strip().isdigit()]
    if royxat:
        return royxat
    royxat = [int(x) for x in (CFG.get("admin_ids") or []) if str(x).isdigit()]
    if royxat:
        return royxat
    bitta = CFG.get("admin_id")
    return [int(bitta)] if bitta else []


TOKEN = str(sozlama("bot_token", "BOT_TOKEN", "")).strip()
ADMINLAR = _adminlar()
BOSH_ADMIN = ADMINLAR[0] if ADMINLAR else 0

PLATFORMA = str(sozlama("platforma_nomi", "PLATFORMA_NOMI", "Chevar AI"))
KOMISSIYA = float(sozlama("komissiya_foiz", "KOMISSIYA_FOIZ", 35) or 35)
OLDINDAN = float(sozlama("oldindan_tolov_foiz", "OLDINDAN_TOLOV_FOIZ", 50) or 50)

KARTA = str(sozlama("karta_raqam", "CARD_NUMBER", ""))
KARTA_EGASI = str(sozlama("karta_egasi", "CARD_OWNER", ""))
ALOQA_TEL = str(sozlama("aloqa_telefon", "SHOP_PHONE", "+998910964410"))
ALOQA_TG = str(sozlama("aloqa_telegram", "SHOP_TELEGRAM", "@diumuser"))

# Yetkazib berish
YETKAZISH_NARX = int(float(sozlama("yetkazish_narx", "YETKAZISH_NARX", 25000) or 25000))
BEPUL_CHEGARA = int(float(sozlama("bepul_yetkazish_chegara", "BEPUL_YETKAZISH", 500000) or 500000))

AI_PROVIDER = str(sozlama("ai_provider", "AI_PROVIDER", "yoq")).lower()
AI_KEY = str(sozlama("ai_key", "AI_KEY", ""))
AI_MODEL = str(sozlama("ai_model", "AI_MODEL", ""))
AI_URL = str(sozlama("ai_url", "AI_URL", ""))

AI_CFG = {"ai_provider": AI_PROVIDER, "ai_key": AI_KEY,
          "ai_model": AI_MODEL, "ai_url": AI_URL}


def admin_mi(uid):
    return int(uid) in ADMINLAR


# =====================  Ma'lumotlar  =====================

DATA = load_json(DATA_FILE, {})
DATA.setdefault("keyingi_raqam", 1001)
DATA.setdefault("foydalanuvchilar", {})
DATA.setdefault("holatlar", {})
DATA.setdefault("buyurtmalar", {})      # AI orqali individual tikish
DATA.setdefault("dizaynlar", {})        # tayyor dizayn namunalari
DATA.setdefault("mahsulotlar", {})      # do'kondagi tayyor mahsulotlar
DATA.setdefault("savatlar", {})         # uid -> [{mahsulot, olcham, soni}]
DATA.setdefault("sotuvlar", {})         # do'kon buyurtmalari
DATA.setdefault("keyingi_sotuv", 5001)
DATA.setdefault("keyingi_dizayn", 1)
DATA.setdefault("keyingi_mahsulot", 1)
DATA.setdefault("offset", 0)

_qulf = threading.Lock()


def saqla():
    with _qulf:
        save_json(DATA_FILE, DATA)


# =====================  Telegram API  =====================

def log(matn):
    qator = "[" + time.strftime("%Y-%m-%d %H:%M:%S") + "] " + str(matn)
    print(qator, flush=True)


def api(method, **params):
    """Telegram API chaqiruvi. Xatoda None qaytaradi (bot to'xtamaydi)."""
    url = API.format(token=TOKEN, method=method)
    data = json.dumps(params).encode("utf-8")
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json"})
    for urinish in range(3):
        try:
            with urllib.request.urlopen(req, timeout=70, context=SSL_CTX) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            try:
                javob = json.loads(e.read().decode("utf-8"))
            except Exception:
                javob = {"description": str(e)}
            if e.code == 429:
                time.sleep(int(javob.get("parameters", {}).get("retry_after", 3)))
                continue
            log("API xato (" + method + "): " + str(javob.get("description")))
            return None
        except Exception as e:
            if urinish == 2:
                log("Ulanish xatosi (" + method + "): " + str(e))
                return None
            time.sleep(2)
    return None


def tugmalar(qatorlar):
    """[[('matn','data'), ...], ...] -> inline klaviatura"""
    return {"inline_keyboard": [[{"text": m, "callback_data": d} for m, d in q]
                                for q in qatorlar]}


def menyu_tugmalari(qatorlar):
    return {"keyboard": [[{"text": m} for m in q] for q in qatorlar],
            "resize_keyboard": True}


def yubor(chat_id, matn, kb=None, menyu=None):
    p = {"chat_id": chat_id, "text": matn, "parse_mode": "HTML",
         "disable_web_page_preview": True}
    if kb:
        p["reply_markup"] = kb
    elif menyu:
        p["reply_markup"] = menyu
    return api("sendMessage", **p)


def rasm_yubor(chat_id, file_id, matn="", kb=None):
    p = {"chat_id": chat_id, "photo": file_id, "parse_mode": "HTML"}
    if matn:
        p["caption"] = matn
    if kb:
        p["reply_markup"] = kb
    return api("sendPhoto", **p)


def tahrirla(chat_id, message_id, matn, kb=None):
    p = {"chat_id": chat_id, "message_id": message_id, "text": matn,
         "parse_mode": "HTML"}
    if kb:
        p["reply_markup"] = kb
    return api("editMessageText", **p)


def javob_ber(callback_id, matn=""):
    api("answerCallbackQuery", callback_query_id=callback_id, text=matn)


def adminlarga(matn, kb=None):
    for a in ADMINLAR:
        yubor(a, matn, kb=kb)


# =====================  Yordamchilar  =====================

def profil(uid):
    p = DATA["foydalanuvchilar"].setdefault(str(uid), {})
    p.setdefault("rol", "mijoz")
    p.setdefault("ism", "")
    p.setdefault("tel", "")
    p.setdefault("shahar", "")
    p.setdefault("manzil", "")
    p.setdefault("ixtisos", "")
    p.setdefault("tasdiq", False)
    p.setdefault("bloklangan", False)
    p.setdefault("qoshildi", time.strftime("%Y-%m-%d"))
    return p


def holat(uid, bosqich=None, **maydonlar):
    h = DATA["holatlar"].setdefault(str(uid), {})
    if bosqich is not None:
        h["bosqich"] = bosqich
    h.update(maydonlar)
    return h


def holat_ol(uid):
    return DATA["holatlar"].get(str(uid), {})


def holat_tozala(uid):
    DATA["holatlar"].pop(str(uid), None)


def pul(son):
    try:
        son = int(round(float(son)))
    except Exception:
        return str(son)
    return "{:,}".format(son).replace(",", " ") + " so'm"


def yaxlit(son, qadam=5000):
    return int((int(son) + qadam - 1) // qadam * qadam)


def mijoz_narxi(usta_narxi):
    """Usta narxi ustiga platforma komissiyasi qo'shiladi."""
    umumiy = float(usta_narxi) / max(0.05, (1.0 - KOMISSIYA / 100.0))
    return yaxlit(umumiy)


def tasdiqlangan_ustalar():
    return [uid for uid, p in DATA["foydalanuvchilar"].items()
            if p.get("rol") == "usta" and p.get("tasdiq") and not p.get("bloklangan")]


def vaqt():
    return time.strftime("%Y-%m-%d %H:%M")
