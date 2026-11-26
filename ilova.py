# -*- coding: utf-8 -*-
"""
Chevar AI — Telegram Mini App (ilova) server qismi.

Bot bilan bitta jarayonda ishlaydi va bitta bazadan foydalanadi:
  /            — ilova (ilova/index.html, app.js, app.css)
  /api/...     — JSON API
  /rasm?f=     — Telegram rasmlarini ilovaga ko'rsatish (proksi, kesh bilan)

Xavfsizlik: foydalanuvchi Telegram bergan initData orqali tanilad (bot tokeni bilan HMAC
tekshiriladi), keyin qisqa muddatli sessiya tokeni beriladi. Har amal egasi/vakolati tekshiriladi.

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

import base64
import hashlib
import hmac
import json
import mimetypes
import os
import threading
import time
import traceback
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import core
from core import (ADMINLAR, DATA, QULF, SSL_CTX, TOKEN, admin_mi, holat, holat_ol, holat_tozala,
                  log, mijoz_narxi, profil, pul, saqla, usta_reyting, vaqt, yubor)

PAPKA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ilova")
SESSIYA_MUDDAT = 12 * 3600
_SIR = hashlib.sha256(("chevar-sessiya:" + TOKEN).encode()).digest()


# =====================  Tanish (auth)  =====================

def initdata_tekshir(init_data, maks_yosh=86400):
    """Telegram WebApp initData ni tekshiradi. To'g'ri bo'lsa — user lug'ati, aks holda None."""
    try:
        juft = dict(urllib.parse.parse_qsl(init_data, keep_blank_values=True))
        h = juft.pop("hash", "")
        satr = "\n".join(k + "=" + v for k, v in sorted(juft.items()))
        kalit = hmac.new(b"WebAppData", TOKEN.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(hmac.new(kalit, satr.encode(), hashlib.sha256).hexdigest(), h):
            return None
        if time.time() - int(juft.get("auth_date", 0)) > maks_yosh:
            return None
        return json.loads(juft.get("user", "{}"))
    except Exception:
        return None


def token_ber(uid):
    muddat = int(time.time()) + SESSIYA_MUDDAT
    xom = str(uid) + "." + str(muddat)
    imzo = hmac.new(_SIR, xom.encode(), hashlib.sha256).hexdigest()[:32]
    return base64.urlsafe_b64encode((xom + "." + imzo).encode()).decode()


def token_uid(token):
    try:
        uid, muddat, imzo = base64.urlsafe_b64decode(token.encode()).decode().split(".")
        kerak = hmac.new(_SIR, (uid + "." + muddat).encode(), hashlib.sha256).hexdigest()[:32]
        if hmac.compare_digest(kerak, imzo) and int(muddat) > time.time():
            return int(uid)
    except Exception:
        pass
    return None


class Xato(Exception):
    def __init__(self, matn, kod=400):
        super().__init__(matn)
        self.kod = kod


# =====================  Yordamchilar  =====================

def _rasm_url(fid, token):
    return ("/rasm?f=" + urllib.parse.quote(fid) + "&t=" + token) if fid else ""


def _tr(uid, matnlar):
    import tarjima
    return tarjima.tez(matnlar, profil(uid).get("til") or "uz")


def _b64_rasm(s):
    if not s:
        return None
    if "," in s[:100]:
        s = s.split(",", 1)[1]
    b = base64.b64decode(s)
    if len(b) > 8 * 1024 * 1024:
        raise Xato("Rasm juda katta (8 MB dan oshmasin)")
    return b


def _yukla(uid, rasm_b64):
    """Rasmni Telegramga yuklab file_id oladi (foydalanuvchining o'z chatiga, keyin o'chiriladi)."""
    b = _b64_rasm(rasm_b64)
    if not b:
        return ""
    return core.rasm_bayt_yuklash(uid, b, "ilova.jpg")


def _usta_info(u, token, tolik=False):
    p = DATA["foydalanuvchilar"].get(str(u), {})
    ort, soni, yakun = usta_reyting(u)
    d = {"id": str(u), "ism": p.get("ism") or "Hunarmand", "shahar": p.get("shahar", ""),
         "ixtisos": p.get("ixtisos", ""), "tajriba": p.get("tajriba", ""),
         "reyting": round(ort, 1), "baholar": soni, "bajarilgan": yakun,
         "pauza": bool(p.get("pauza")),
         "portfolio": [_rasm_url(r["rasm"], token) for r in p.get("portfolio", [])[:10]]}
    if tolik:
        d["sharhlar"] = [{"baho": s["baho"], "matn": s.get("matn", ""), "mijoz": s.get("mijoz", ""),
                          "sana": s.get("sana", ""), "kiyim": s.get("kiyim", "")}
                         for s in p.get("sharhlar", [])[::-1][:20]]
    return d


def _kuzatuv(b):
    import kuzatuv
    joriy = kuzatuv._joriy(b)
    vaqtlar = dict(b.get("vaqtlar", {}))
    vaqtlar.setdefault("yuborildi", vaqtlar.get("qabul") or b.get("yaratildi", ""))
    return [{"kalit": k, "nom": nom, "holat": ("otdi" if i < joriy or (i == joriy == len(kuzatuv.BOSQICHLAR) - 1)
                                              else "joriy" if i == joriy else "keyin"),
             "vaqt": vaqtlar.get(k, "")} for i, (k, nom) in enumerate(kuzatuv.BOSQICHLAR)]


def _buyurtma(b, uid, token):
    import bot
    import suhbat
    karta = b.get("karta") or {}
    tur = karta.get("tur")
    maydonlar = [{"nom": suhbat.MAYDON_NOMI.get(k, k), "qiymat": karta.get("maydonlar", {}).get(k)}
                 for k, _ in suhbat.TURLAR.get(tur or "", {}).get("maydonlar", [])
                 if karta.get("maydonlar", {}).get(k)]
    if not karta:
        maydonlar = [{"nom": suhbat.MAYDON_NOMI.get(k, k), "qiymat": v}
                     for k, v in (b.get("tafsilot") or {}).items() if v and k not in ("izoh", "tur")]
    d = {"raqam": b["raqam"], "holat": b["holat"], "holat_nomi": bot.holat_nomi(b),
         "mahsulot": suhbat.TURLAR.get(tur or "", {}).get("nom") or (b.get("tafsilot") or {}).get("kiyim", "buyurtma"),
         "maydonlar": maydonlar, "olcham": b.get("olcham") or {}, "muddat": b.get("muddat", ""),
         "yaratildi": b.get("yaratildi", ""), "narx": b.get("umumiy_narx", 0),
         "muddat_kun": b.get("muddat_kun"), "kuzatuv": _kuzatuv(b),
         "tayyor_rasm": _rasm_url(b.get("tayyor_rasm", ""), token),
         "dizayn_rasm": _rasm_url(b.get("dizayn_rasm", ""), token),
         "tolov": {"oldindan": b["tolov"].get("oldindan", 0), "qolgan": b["tolov"].get("qolgan", 0),
                   "holat": b["tolov"].get("holat", "")},
         "baho": b.get("baho"), "usta": _usta_info(b["usta"], token) if b.get("usta") else None}
    # Foydalanuvchi tiliga (kaa/en/kirill) tarjima — faqat tayyor tarjimalar, kutmasdan
    asl = [d["holat_nomi"], d["mahsulot"]] + [m["nom"] for m in d["maydonlar"]] + [q["nom"] for q in d["kuzatuv"]]
    tr = _tr(uid, asl)
    d["holat_nomi"], d["mahsulot"] = tr[0], tr[1]
    for i, m in enumerate(d["maydonlar"]):
        m["nom"] = tr[2 + i]
    for i, q in enumerate(d["kuzatuv"]):
        q["nom"] = tr[2 + len(d["maydonlar"]) + i]
    if str(b["mijoz"]) == str(uid):
        d["takliflar"] = [dict(t, usta=_usta_info(u, token), usta_id=u, narx=t.get("mijoz_narx"))
                          for u, t in b.get("takliflar", {}).items()] if b["holat"] == "yangi" else []
    return d


# =====================  API: umumiy va mijoz  =====================

def api_kirish(uid, d, token):
    p = profil(uid)
    if d.get("_user"):
        u = d["_user"]
        if not p.get("ism"):
            p["ism"] = ((u.get("first_name") or "") + " " + (u.get("last_name") or "")).strip()
        if u.get("username"):
            p["username"] = u["username"]
        if not p.get("til"):
            lc = (u.get("language_code") or "").lower()
            p["til"] = "en" if lc.startswith("en") else "uz"
    p["oxirgi"] = vaqt()
    saqla()
    from core import ALOQA_TEL, ALOQA_TG, KARTA, KARTA_EGASI, OLDINDAN, KOMISSIYA, \
        YETKAZISH_NARX, BEPUL_CHEGARA, PLATFORMA
    return {"token": token, "uid": str(uid), "ism": p.get("ism", ""), "til": p.get("til") or "uz",
            "tel": p.get("tel", ""), "manzil": p.get("manzil", ""), "rol": p.get("rol", "mijoz"),
            "tasdiq": bool(p.get("tasdiq")), "pauza": bool(p.get("pauza")), "admin": admin_mi(uid),
            "olchamlar": p.get("olchamlar", {}), "sevimlilar": p.get("sevimlilar", []),
            "sozlama": {"platforma": PLATFORMA, "karta": KARTA, "karta_egasi": KARTA_EGASI,
                        "oldindan": OLDINDAN, "komissiya": KOMISSIYA, "yetkazish": YETKAZISH_NARX,
                        "bepul": BEPUL_CHEGARA, "tel": ALOQA_TEL, "tg": ALOQA_TG,
                        "bot": core.BOT_USERNAME}}


def api_turlar(uid, d, token):
    import suhbat
    asl = []
    for v in suhbat.TURLAR.values():
        asl.append(v["nom"])
        asl += ["❓ " + q for _, q in v["maydonlar"]]
    mn = list(suhbat.MAYDON_NOMI.items())
    tr = iter(_tr(uid, asl + [x for _, x in mn]))
    turlar = {}
    for k, v in suhbat.TURLAR.items():
        nom = next(tr)
        turlar[k] = {"nom": nom, "olcham": v["olcham"],
                     "maydonlar": [{"kalit": m, "savol": next(tr).lstrip("❓ ").strip()} for m, _ in v["maydonlar"]]}
    return {"turlar": turlar, "maydon_nomi": {k: next(tr) for k, _ in mn},
            "olcham_savol": suhbat.OLCHAM_SAVOL,
            "variantlar": {m: list(v.keys()) for m, v in suhbat.QIYMAT_SOZLAR.items()}}


def api_ai_ajrat(uid, d, token):
    """Erkin matndan karta — bazaga tegmaydi, shuning uchun QULF'siz (AI 12 soniyagacha)."""
    import suhbat
    karta = d.get("karta") or suhbat.yangi_karta()
    karta.setdefault("maydonlar", {})
    matn = (d.get("matn") or "").strip()[:600]
    if matn:
        suhbat.javobni_qabul(core.AI_CFG, matn, karta)
    ks = suhbat.keyingi_savol(karta)
    return {"karta": karta, "keyingi": ks[0] if ks else None}


def api_buyurtma(uid, d, token):
    import bot
    import suhbat
    karta = d.get("karta") or {}
    if karta.get("tur") not in suhbat.TURLAR:
        raise Xato("Mahsulot turi tanlanmagan")
    tel = (d.get("tel") or profil(uid).get("tel") or "").replace(" ", "")
    if len(tel) < 7:
        raise Xato("Telefon raqamni kiriting")
    olcham = {k: str(v)[:20] for k, v in (d.get("olcham") or {}).items()
              if k in ("razmer", "boy", "kokrak", "bel", "son") and v}
    dz = DATA["dizaynlar"].get(d.get("dizayn") or "")
    holat(uid, "yakuniy", karta={"tur": karta["tur"], "oxirgi": None,
                                 "maydonlar": {k: str(v)[:120] for k, v in karta.get("maydonlar", {}).items() if v},
                                 "izoh": (karta.get("izoh") or "")[:300]},
          olcham=olcham, muddat=(d.get("muddat") or "")[:60], tel=tel,
          dizayn=dz["id"] if dz else "", dizayn_rasm=dz.get("rasm", "") if dz else "")
    p = profil(uid)
    if p.get("rol") != "usta":
        p["tel"] = tel
    oldin = DATA["keyingi_raqam"]
    bot.buyurtma_yarat(uid)
    return {"raqam": str(oldin)}


def api_buyurtmalarim(uid, d, token):
    import dokon
    tikish = [_buyurtma(b, uid, token) for b in sorted(DATA["buyurtmalar"].values(), key=lambda x: -int(x["raqam"]))
              if str(b["mijoz"]) == str(uid)]
    sotuv = [dict(s, holat_nomi=_sotuv_holat(s["holat"])) for s in
             sorted(DATA["sotuvlar"].values(), key=lambda x: -int(x["raqam"])) if str(s["mijoz"]) == str(uid)]
    for s in sotuv:
        s.pop("chek", None)
    return {"tikish": tikish, "sotuv": sotuv}


def _sotuv_holat(h):
    return {"tolov_kutilmoqda": "💳 To'lov kutilmoqda", "tekshiruvda": "🔍 Chek tekshirilmoqda",
            "tolangan": "📦 Tayyorlanmoqda", "yolda": "🚚 Yo'lda", "topshirildi": "✅ Topshirildi",
            "bekor": "❌ Bekor"}.get(h, h)


def _mening(uid, raqam):
    b = DATA["buyurtmalar"].get(str(raqam))
    if not b or str(b["mijoz"]) != str(uid):
        raise Xato("Buyurtma topilmadi", 404)
    return b


def api_taklif_tanla(uid, d, token):
    import bot
    b = _mening(uid, d.get("raqam"))
    if b["holat"] != "yangi" or str(d.get("usta")) not in b.get("takliflar", {}):
        raise Xato("Bu taklifni tanlab bo'lmaydi")
    bot.usta_tanlandi(uid, b["raqam"], str(d["usta"]))
    return {"ok": True}


def api_chek(uid, d, token):
    import bot
    tur = d.get("tur")
    fid = _yukla(uid, d.get("rasm"))
    if not fid:
        raise Xato("Chek rasmini tanlang")
    if tur == "sotuv":
        s = DATA["sotuvlar"].get(str(d.get("raqam")))
        if not s or str(s["mijoz"]) != str(uid) or s["holat"] != "tolov_kutilmoqda":
            raise Xato("Bu buyurtma uchun to'lov kutilmayapti")
        bot.sotuv_chek_saqla(uid, s["raqam"], fid)
    else:
        b = _mening(uid, d.get("raqam"))
        if (tur == "oldindan" and b["holat"] != "tasdiqlangan") or (tur == "qolgan" and b["holat"] != "tayyor"):
            raise Xato("Bu bosqichda to'lov kutilmayapti")
        if b["tolov"].get("holat", "").endswith("tekshiruvda"):
            raise Xato("Chek allaqachon tekshirilmoqda")
        bot.chek_saqla(uid, b["raqam"], tur, fid)
    return {"ok": True}


def api_olindi(uid, d, token):
    import bot
    b = _mening(uid, d.get("raqam"))
    if not bot.topshirildi(b["raqam"], "mijoz"):
        raise Xato("Bu buyurtma yetkazilmoqda holatida emas")
    return {"ok": True}


def api_baho(uid, d, token):
    import kuzatuv
    b = _mening(uid, d.get("raqam"))
    ball = int(d.get("ball") or 0)
    if b["holat"] != "yakunlandi" or b.get("baho") or not 1 <= ball <= 5 or not b.get("usta"):
        raise Xato("Baho qo'yib bo'lmaydi")
    profil(b["usta"]).setdefault("baholar", []).append(ball)
    b["baho"] = ball
    kuzatuv.sharh_qosh(b["usta"], b, ball, core.esc((d.get("matn") or "").strip())[:400])
    saqla()
    yubor(b["usta"], "⭐️ Sizga yangi baho: " + "⭐️" * ball
          + ("\n💬 «" + core.esc(d["matn"][:400]) + "»" if d.get("matn") else ""))
    return {"ok": True}


def api_bekor(uid, d, token):
    b = _mening(uid, d.get("raqam"))
    if b["holat"] not in ("yangi", "tasdiqlangan") or str(b["tolov"].get("holat", "")).endswith("tekshiruvda"):
        raise Xato("Bu buyurtmani endi bekor qilib bo'lmaydi")
    b["holat"] = "bekor"
    saqla()
    if b.get("usta"):
        yubor(b["usta"], "ℹ️ Mijoz #" + b["raqam"] + " buyurtmasini bekor qildi.")
    return {"ok": True}


def api_yoz(uid, d, token):
    """Mijoz ⇄ usta xabari (ilovadan). Taklif bosqichida ham, ish davomida ham."""
    from core import tugmalar
    b = DATA["buyurtmalar"].get(str(d.get("raqam")))
    matn = core.esc((d.get("matn") or "").strip())[:1000]
    if not b or not matn:
        raise Xato("Xabar bo'sh")
    if str(uid) == str(b["mijoz"]):
        kimga = str(d.get("usta") or b.get("usta") or "")
        if kimga not in b.get("takliflar", {}) and kimga != str(b.get("usta")):
            raise Xato("Hunarmand topilmadi")
        sarlavha = "✉️ <b>Mijozdan xabar</b> (#" + b["raqam"] + ")"
        kb = tugmalar([[("↩️ Javob berish", "jav_" + b["raqam"] + "_" + str(uid))]])
    elif str(uid) == str(b.get("usta")) or str(uid) in b.get("takliflar", {}):
        kimga = str(b["mijoz"])
        sarlavha = "✉️ <b>Hunarmanddan xabar</b> (#" + b["raqam"] + ")"
        kb = tugmalar([[("↩️ Javob berish", "sav_" + b["raqam"] + "_" + str(uid))]])
    else:
        raise Xato("Ruxsat yo'q", 403)
    yubor(int(kimga), sarlavha + "\n\n" + matn, kb=kb)
    b.setdefault("yozishuv", []).append({"kim": "mijoz" if str(uid) == str(b["mijoz"]) else "usta",
                                         "vaqt": vaqt(), "matn": matn})
    saqla()
    return {"ok": True}


def api_dizaynlar(uid, d, token):
    import dokon
    royxat = sorted(dokon.faol_dizaynlar(), key=dokon._kod_tartib)
    sev = set(profil(uid).get("sevimlilar", []))
    nomlar = _tr(uid, [x.get("nom", "") for x in royxat] + [x.get("tavsif", "") for x in royxat])
    n = len(royxat)
    return {"dizaynlar": [{"id": x["id"], "nom": nomlar[i], "tavsif": nomlar[n + i],
                           "mato": x.get("mato", ""), "rang": x.get("rang", ""),
                           "kategoriya": x.get("kategoriya") or "Boshqa", "uslub": dokon._uslub(x),
                           "narx": x.get("narx", 0), "rasm": _rasm_url(x.get("rasm", ""), token),
                           "sevimli": ("d:" + x["id"]) in sev} for i, x in enumerate(royxat)]}


def api_dizayn_karta(uid, d, token):
    import suhbat
    x = DATA["dizaynlar"].get(d.get("id") or "")
    if not x:
        raise Xato("Dizayn topilmadi", 404)
    return {"karta": suhbat.dizayndan(x)}


def api_mahsulotlar(uid, d, token):
    import dokon
    sev = set(profil(uid).get("sevimlilar", []))
    return {"mahsulotlar": [{"id": m["id"], "nom": m.get("nom", ""), "tavsif": m.get("tavsif", ""),
                             "narx": m.get("narx", 0), "kategoriya": m.get("kategoriya") or "Boshqa",
                             "sotuvchi": m.get("sotuvchi") or "Chevar AI do'koni",
                             "zaxira": {k: int(v) for k, v in (m.get("zaxira") or {}).items() if int(v) > 0},
                             "rasm": _rasm_url(m.get("rasm", ""), token), "sevimli": ("m:" + m["id"]) in sev}
                            for m in dokon.faol_mahsulotlar()]}


def _savat_javob(uid, token):
    import dokon
    from core import YETKAZISH_NARX, BEPUL_CHEGARA
    q = []
    for i, x in enumerate(DATA["savatlar"].get(str(uid), [])):
        m = DATA["mahsulotlar"].get(x["mahsulot"])
        if m:
            q.append({"indeks": i, "id": m["id"], "nom": m["nom"], "olcham": x["olcham"], "soni": x["soni"],
                      "narx": m.get("narx", 0), "rasm": _rasm_url(m.get("rasm", ""), token),
                      "bor": int((m.get("zaxira") or {}).get(x["olcham"], 0))})
    jami = dokon.savat_jami(uid)
    return {"savat": q, "jami": jami, "yetkazish": 0 if jami >= BEPUL_CHEGARA else YETKAZISH_NARX}


def api_savat(uid, d, token):
    amal = d.get("amal")
    savat = DATA["savatlar"].setdefault(str(uid), [])
    if amal == "qosh":
        m = DATA["mahsulotlar"].get(d.get("id") or "")
        o = d.get("olcham")
        if not m or not m.get("faol", True) or int((m.get("zaxira") or {}).get(o, 0)) <= 0:
            raise Xato("Bu o'lcham tugagan")
        for x in savat:
            if x["mahsulot"] == m["id"] and x["olcham"] == o:
                if x["soni"] + 1 > int(m["zaxira"][o]):
                    raise Xato("Bu o'lchamdan boshqa qolmagan")
                x["soni"] += 1
                break
        else:
            savat.append({"mahsulot": m["id"], "olcham": o, "soni": 1})
    elif amal in ("kop", "kam", "och"):
        i = int(d.get("indeks", -1))
        if not 0 <= i < len(savat):
            raise Xato("Topilmadi")
        x = savat[i]
        bor = int((DATA["mahsulotlar"].get(x["mahsulot"], {}).get("zaxira") or {}).get(x["olcham"], 0))
        if amal == "kop":
            if x["soni"] + 1 > bor:
                raise Xato("Bu o'lchamdan " + str(bor) + " ta qolgan")
            x["soni"] += 1
        elif amal == "kam":
            x["soni"] -= 1
            if x["soni"] <= 0:
                savat.pop(i)
        else:
            savat.pop(i)
    elif amal == "toza":
        savat.clear()
    saqla()
    return _savat_javob(uid, token)


def api_rasmiylashtir(uid, d, token):
    import dokon
    if not DATA["savatlar"].get(str(uid)):
        raise Xato("Savat bo'sh")
    usul = "olib" if d.get("usul") == "olib" else "yetkazish"
    tel = (d.get("tel") or "").replace(" ", "")
    manzil = (d.get("manzil") or "").strip()[:300]
    if len(tel) < 7 or (usul == "yetkazish" and len(manzil) < 5):
        raise Xato("Telefon va manzilni to'liq kiriting")
    p = profil(uid)
    if p.get("rol") != "usta":
        p["tel"] = tel
    if manzil:
        p["manzil"] = manzil
    holat(uid, "sotuv_tel", usul=usul, manzil=core.esc(manzil), tel=tel)
    oldin = DATA["keyingi_sotuv"]
    dokon.sotuv_yarat(uid)
    if DATA["keyingi_sotuv"] == oldin:
        raise Xato("Ba'zi mahsulotlar tugab qolgan — savatni yangilang")
    return {"raqam": str(oldin)}


def api_kataloglar(uid, d, token):
    import katalog
    return {"matolar": katalog.MATOLAR,
            "olcham": {"ayol": katalog.AYOL, "erkak": katalog.ERKAK, "bola": katalog.BOLA},
            "hunarlar": katalog.HUNARLAR,
            "darslar": [{"hunar": x["hunar"], "nom": x["nom"], "tavsif": x.get("tavsif", ""),
                         "havola": x.get("havola", ""), "video": bool(x.get("video")), "id": x.get("id")}
                        for x in DATA.get("darslar", [])],
            "qidiruv": {h: "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q)
                        for h, q in katalog.QIDIRUV.items()}}


def api_dars_video(uid, d, token):
    """Video darsni foydalanuvchining Telegram chatiga yuboradi (katta videolarni ilovada o'ynatish o'rniga)."""
    x = next((x for x in DATA.get("darslar", []) if x.get("id") == d.get("id")), None)
    if not x or not x.get("video"):
        raise Xato("Dars topilmadi", 404)
    core.api("sendVideo", chat_id=uid, video=x["video"], caption="▶️ " + x["nom"])
    return {"ok": True}


def api_maslahat(uid, d, token):
    import katalog
    jins = d.get("jins")
    boy, vazn = int(d.get("boy") or 0), int(d.get("vazn") or 0)
    if jins not in ("ayol", "erkak", "bola") or not 60 <= boy <= 220 or (jins != "bola" and not 25 <= vazn <= 200):
        raise Xato("Bo'y (sm) va vaznni (kg) to'g'ri kiriting")
    izoh, v = katalog.tavsiya(jins, boy, vazn)
    return {"izoh": izoh, "variantlar": v}


def api_ustalar(uid, d, token):
    ustalar = [u for u, p in DATA["foydalanuvchilar"].items()
               if p.get("rol") == "usta" and p.get("tasdiq") and not p.get("bloklangan")]
    royxat = [_usta_info(u, token, tolik=True) for u in ustalar]
    royxat.sort(key=lambda x: (-x["reyting"], -x["bajarilgan"]))
    return {"ustalar": royxat}


def api_profil(uid, d, token):
    p = profil(uid)
    import tarjima
    if d.get("til") in tarjima.TILLAR:
        p["til"] = d["til"]
    for k, n in (("ism", 60), ("manzil", 300)):
        if k in d:
            p[k] = core.esc(str(d[k]).strip())[:n]
    if "tel" in d and p.get("rol") != "usta":
        p["tel"] = str(d["tel"]).replace(" ", "")[:20]
    if "olchamlar" in d:  # saqlangan o'lchamlar (qo'shimcha imkoniyat)
        p["olchamlar"] = {k: str(v)[:20] for k, v in (d["olchamlar"] or {}).items()
                          if k in ("razmer", "boy", "kokrak", "bel", "son") and v}
    saqla()
    return api_kirish(uid, {}, token)


def api_sevimli(uid, d, token):
    p = profil(uid)
    kalit = str(d.get("kalit") or "")[:40]
    if not kalit.startswith(("d:", "m:")):
        raise Xato("Noto'g'ri")
    s = p.setdefault("sevimlilar", [])
    if kalit in s:
        s.remove(kalit)
    else:
        s.append(kalit)
    saqla()
    return {"sevimlilar": s}


def api_operator(uid, d, token):
    import bot
    matn = core.esc((d.get("matn") or "").strip())[:1500]
    if not matn:
        raise Xato("Xabarni yozing")
    holat(uid, "operator", operator_izoh="Ilovadan")
    bot.operatorga_yubor(uid, matn)
    return {"ok": True}


# =====================  API: hunarmand  =====================

def _usta(uid):
    p = profil(uid)
    if p.get("rol") != "usta" or not p.get("tasdiq") or p.get("bloklangan"):
        raise Xato("Faqat tasdiqlangan hunarmandlar uchun", 403)
    return p


def api_usta_royxat(uid, d, token):
    import bot
    p = profil(uid)
    if p.get("rol") == "usta":
        raise Xato("Ariza allaqachon yuborilgan" if not p.get("tasdiq") else "Siz allaqachon hunarmandsiz")
    maydon = {k: core.esc(str(d.get(k) or "").strip())[:120] for k in ("ism", "shahar", "ixtisos", "tajriba", "tel")}
    if not all(maydon.values()):
        raise Xato("Barcha maydonlarni to'ldiring")
    holat(uid, "usta_reg", usta_indeks=len(bot.USTA_SAVOLLARI) - 1,
          usta={k: maydon[k] for k in ("ism", "shahar", "ixtisos", "tajriba")})
    bot.usta_reg_davom(uid, maydon["tel"])
    return api_kirish(uid, {}, token)


def api_usta_buyurtmalar(uid, d, token):
    _usta(uid)
    ochiq = [_buyurtma(b, uid, token) for b in sorted(DATA["buyurtmalar"].values(), key=lambda x: -int(x["raqam"]))
             if b["holat"] == "yangi" and str(uid) not in b["takliflar"]
             and str(uid) not in b.get("rad_etganlar", [])]
    ishlar = []
    for b in sorted(DATA["buyurtmalar"].values(), key=lambda x: -int(x["raqam"])):
        if str(b.get("usta")) == str(uid):
            x = _buyurtma(b, uid, token)
            x["usta_narx"] = b.get("usta_narx", 0)
            x["mijoz_tel"] = b.get("mijoz_tel", "") if b["holat"] not in ("yangi", "bekor") else ""
            ishlar.append(x)
    takliflarim = [dict(_buyurtma(b, uid, token), mening_taklif=b["takliflar"][str(uid)])
                   for b in DATA["buyurtmalar"].values() if b["holat"] == "yangi" and str(uid) in b["takliflar"]]
    p = profil(uid)
    return {"ochiq": ochiq, "ishlar": ishlar, "takliflarim": takliflarim,
            "men": _usta_info(uid, token, tolik=True), "pauza": bool(p.get("pauza")),
            "daromad": sum(b.get("usta_narx", 0) for b in DATA["buyurtmalar"].values()
                           if str(b.get("usta")) == str(uid) and b["holat"] == "yakunlandi")}


def api_usta_taklif(uid, d, token):
    import bot
    import kuzatuv
    _usta(uid)
    b = DATA["buyurtmalar"].get(str(d.get("raqam")))
    narx, kun = int(d.get("narx") or 0), int(d.get("kun") or 0)
    if not b or b["holat"] != "yangi":
        raise Xato("Bu buyurtma yopilgan")
    if narx < 10000 or not 1 <= kun <= 365:
        raise Xato("Narx (kamida 10 000) va kunlar sonini to'g'ri kiriting")
    if not b.get("korilmoqda"):
        b["korilmoqda"] = True
    holat(uid, "narx_izoh", narx_raqam=b["raqam"], narx_qiymat=narx, narx_kun=kun)
    bot.izoh_qabul(uid, core.esc((d.get("izoh") or "-").strip())[:300] or "-")
    return {"ok": True, "mijoz_narx": mijoz_narxi(narx)}


def api_usta_rad(uid, d, token):
    _usta(uid)
    b = DATA["buyurtmalar"].get(str(d.get("raqam")))
    if b:
        b.setdefault("rad_etganlar", [])
        if str(uid) not in b["rad_etganlar"]:
            b["rad_etganlar"].append(str(uid))
        saqla()
    return {"ok": True}


def api_usta_tayyor(uid, d, token):
    import bot
    _usta(uid)
    b = DATA["buyurtmalar"].get(str(d.get("raqam")))
    if not b or str(b.get("usta")) != str(uid) or b["holat"] != "tikilmoqda":
        raise Xato("Bu buyurtma «tikilmoqda» holatida emas")
    fid = _yukla(uid, d.get("rasm")) if d.get("rasm") else ""
    bot.ish_tayyor(uid, b["raqam"], fid)
    return {"ok": True}


def api_usta_pauza(uid, d, token):
    p = _usta(uid)
    p["pauza"] = not p.get("pauza")
    saqla()
    return {"pauza": p["pauza"]}


def api_usta_portfolio(uid, d, token):
    p = _usta(uid)
    if d.get("amal") == "toza":
        p["portfolio"] = []
    else:
        if len(p.get("portfolio", [])) >= 10:
            raise Xato("Portfolio to'la (10 ta)")
        fid = _yukla(uid, d.get("rasm"))
        p.setdefault("portfolio", []).append({"rasm": fid, "izoh": "", "vaqt": vaqt()})
    saqla()
    return {"portfolio": [_rasm_url(r["rasm"], token) for r in p.get("portfolio", [])]}


def api_usta_profil(uid, d, token):
    p = _usta(uid)
    for k in ("ism", "shahar", "ixtisos", "tajriba", "tel"):
        if d.get(k):
            p[k] = core.esc(str(d[k]).strip())[:120]
    saqla()
    return {"men": _usta_info(uid, token, tolik=True)}


# =====================  API: admin  =====================

def _admin(uid):
    if not admin_mi(uid):
        raise Xato("Faqat adminlar uchun", 403)


def api_admin_holat(uid, d, token):
    _admin(uid)
    bs = list(DATA["buyurtmalar"].values())
    ss = list(DATA["sotuvlar"].values())
    yakun = [b for b in bs if b["holat"] == "yakunlandi"]
    sotildi = [s for s in ss if s["holat"] in ("tolangan", "yolda", "topshirildi")]
    ustalar = [(u, p) for u, p in DATA["foydalanuvchilar"].items() if p.get("rol") == "usta"]
    tolovlar = []
    for b in bs:
        th = b["tolov"].get("holat", "")
        if th.endswith("tekshiruvda"):
            tur = "oldindan" if th.startswith("oldindan") else "qolgan"
            tolovlar.append({"tur": "tikish", "chek_tur": tur, "raqam": b["raqam"],
                             "summa": b["tolov"].get(tur, 0), "mijoz": str(b["mijoz"]),
                             "rasm": _rasm_url(b["tolov"].get("chek_" + tur, ""), token)})
    for s in ss:
        if s["holat"] == "tekshiruvda":
            tolovlar.append({"tur": "sotuv", "raqam": s["raqam"], "summa": s["umumiy"],
                             "mijoz": str(s["mijoz"]), "rasm": _rasm_url(s.get("chek", ""), token)})
    return {
        "stat": {"foydalanuvchi": len(DATA["foydalanuvchilar"]), "usta": len(ustalar),
                 "kutayotgan": sum(1 for _, p in ustalar if not p.get("tasdiq")),
                 "buyurtma": len(bs), "yakunlangan": len(yakun),
                 "aylanma": sum(b.get("umumiy_narx", 0) for b in yakun),
                 "foyda": sum(b.get("umumiy_narx", 0) - b.get("usta_narx", 0) for b in yakun),
                 "sotuv": len(ss), "dokon_aylanma": sum(s.get("umumiy", 0) for s in sotildi),
                 "mahsulot": len(DATA["mahsulotlar"]), "dizayn": len(DATA["dizaynlar"])},
        "tolovlar": tolovlar,
        "buyurtmalar": [_buyurtma(b, uid, token) for b in sorted(bs, key=lambda x: -int(x["raqam"]))
                        if b["holat"] not in ("yakunlandi", "bekor")][:40],
        "sotuvlar": [dict(s, holat_nomi=_sotuv_holat(s["holat"]), chek=_rasm_url(s.get("chek", ""), token))
                     for s in sorted(ss, key=lambda x: -int(x["raqam"])) if s["holat"] not in ("topshirildi", "bekor")][:40],
        "ustalar": [dict(_usta_info(u, token, tolik=True), tasdiq=bool(p.get("tasdiq")),
                         bloklangan=bool(p.get("bloklangan")), tel=p.get("tel", ""),
                         username=p.get("username", "")) for u, p in ustalar],
        "foydalanuvchilar": sorted([{"id": u, "ism": p.get("ism", ""), "username": p.get("username", ""),
                                     "tel": p.get("tel", ""), "til": p.get("til") or "uz", "rol": p.get("rol"),
                                     "oxirgi": p.get("oxirgi", ""), "bloklangan": bool(p.get("bloklangan")),
                                     "buyurtma": sum(1 for b in bs if str(b["mijoz"]) == u)}
                                    for u, p in DATA["foydalanuvchilar"].items()],
                                   key=lambda x: x["oxirgi"] or "", reverse=True),
        "mahsulotlar": [{"id": m["id"], "nom": m.get("nom"), "narx": m.get("narx"), "faol": m.get("faol", True),
                         "zaxira": m.get("zaxira", {})} for m in DATA["mahsulotlar"].values()],
        "dizaynlar": [{"id": x["id"], "nom": x.get("nom"), "faol": x.get("faol", True)}
                      for x in DATA["dizaynlar"].values()],
    }


def api_admin_amal(uid, d, token):
    """Bitta joydan: to'lov, usta, foydalanuvchi, do'kon holati, topshirildi, yashirish."""
    import bot
    import dokon
    _admin(uid)
    amal, x = d.get("amal"), str(d.get("id") or "")
    if amal == "tolov_ha":
        ok = bot.tolov_tasdiq(x, d.get("chek_tur"))
    elif amal == "tolov_yoq":
        b = DATA["buyurtmalar"].get(x)
        ok = bool(b and b["tolov"].get("holat", "").endswith("tekshiruvda"))
        if ok:
            b["tolov"]["holat"] = "rad"
            yubor(b["mijoz"], "❗️ To'lov cheki tasdiqlanmadi. Qayta tekshirib yuboring yoki biz bilan bog'laning.")
    elif amal in ("tolangan", "yolda", "topshirildi_s", "bekor_s"):
        ok = dokon.sotuv_holat_ozgartir(x, {"topshirildi_s": "topshirildi", "bekor_s": "bekor"}.get(amal, amal))
    elif amal == "topshirildi":
        ok = bot.topshirildi(x, "admin")
    elif amal in ("usta_tasdiq", "usta_rad"):
        p = profil(x)
        p["rol"] = "usta" if amal == "usta_tasdiq" else "mijoz"
        p["tasdiq"] = amal == "usta_tasdiq"
        ok = True
        yubor(int(x), "🎉 Siz hunarmand sifatida tasdiqlandingiz! Yangi buyurtmalar endi sizga keladi."
              if p["tasdiq"] else "Afsuski, arizangiz tasdiqlanmadi.")
    elif amal == "blok":
        if admin_mi(x):
            raise Xato("Adminni bloklab bo'lmaydi")
        p = profil(x)
        p["bloklangan"] = not p.get("bloklangan")
        ok = True
    elif amal in ("dizayn_faol", "mahsulot_faol"):
        jadval = DATA["dizaynlar" if amal == "dizayn_faol" else "mahsulotlar"]
        ok = x in jadval
        if ok:
            jadval[x]["faol"] = not jadval[x].get("faol", True)
    else:
        raise Xato("Noma'lum amal")
    saqla()
    if not ok:
        raise Xato("Bu amal allaqachon bajarilgan yoki hozir mumkin emas")
    return {"ok": True}


def api_admin_qosh(uid, d, token):
    """Mahsulot yoki dizayn qo'shish (rasm bilan)."""
    _admin(uid)
    tur = d.get("tur")
    nom = core.esc((d.get("nom") or "").strip())[:120]
    if not nom:
        raise Xato("Nomini kiriting")
    fid = _yukla(uid, d.get("rasm")) if d.get("rasm") else ""
    yangi = {"nom": nom, "tavsif": core.esc((d.get("tavsif") or "").strip())[:400],
             "kategoriya": core.esc((d.get("kategoriya") or "").strip())[:60], "rasm": fid,
             "faol": True, "qoshildi": vaqt()}
    if tur == "mahsulot":
        zaxira = {}
        for bolak in str(d.get("zaxira") or "").replace(";", ",").split(","):
            if ":" in bolak:
                o, s = bolak.split(":", 1)
                if o.strip() and s.strip().isdigit():
                    zaxira[o.strip().upper()] = int(s)
        if not zaxira or int(d.get("narx") or 0) <= 0:
            raise Xato("Narx va o'lchamlarni (S:2, M:3) kiriting")
        kod = "M" + str(DATA["keyingi_mahsulot"])
        DATA["keyingi_mahsulot"] += 1
        yangi.update(id=kod, narx=int(d["narx"]), zaxira=zaxira,
                     sotuvchi=core.esc((d.get("sotuvchi") or "").strip())[:80])
        DATA["mahsulotlar"][kod] = yangi
    elif tur == "dizayn":
        kod = "D" + str(DATA["keyingi_dizayn"])
        DATA["keyingi_dizayn"] += 1
        yangi.update(id=kod, mato=core.esc(d.get("mato") or "")[:60], rang=core.esc(d.get("rang") or "")[:60],
                     kiyim=core.esc(d.get("kiyim") or "")[:60], narx=int(d.get("narx") or 0),
                     uslub="Qoraqalpoq" if d.get("uslub") == "Qoraqalpoq" else "O'zbek")
        DATA["dizaynlar"][kod] = yangi
    elif tur == "dars":
        import katalog
        if d.get("hunar") not in katalog.HUNARLAR or not str(d.get("havola", "")).startswith("http"):
            raise Xato("Hunar va havolani kiriting")
        DATA.setdefault("darslar", []).append({"hunar": d["hunar"], "nom": nom, "tavsif": yangi["tavsif"],
                                               "havola": d["havola"][:300], "video": "",
                                               "id": len(DATA["darslar"]) + 1, "qoshildi": vaqt()})
        kod = "dars"
    else:
        raise Xato("Noma'lum tur")
    saqla()
    return {"id": kod}


def api_admin_zaxira(uid, d, token):
    import zaxira
    _admin(uid)
    return {"ok": zaxira.zaxira_yubor(uid, "ilovadan")}


YOLLAR = {
    "turlar": api_turlar, "buyurtma": api_buyurtma, "buyurtmalarim": api_buyurtmalarim,
    "taklif_tanla": api_taklif_tanla, "chek": api_chek, "olindi": api_olindi, "baho": api_baho,
    "bekor": api_bekor, "yoz": api_yoz, "dizaynlar": api_dizaynlar, "dizayn_karta": api_dizayn_karta,
    "mahsulotlar": api_mahsulotlar, "savat": api_savat, "rasmiylashtir": api_rasmiylashtir,
    "kataloglar": api_kataloglar, "dars_video": api_dars_video, "maslahat": api_maslahat,
    "ustalar": api_ustalar, "profil": api_profil, "sevimli": api_sevimli, "operator": api_operator,
    "usta/royxat": api_usta_royxat, "usta/buyurtmalar": api_usta_buyurtmalar, "usta/taklif": api_usta_taklif,
    "usta/rad": api_usta_rad, "usta/tayyor": api_usta_tayyor, "usta/pauza": api_usta_pauza,
    "usta/portfolio": api_usta_portfolio, "usta/profil": api_usta_profil,
    "admin/holat": api_admin_holat, "admin/amal": api_admin_amal, "admin/qosh": api_admin_qosh,
    "admin/zaxira": api_admin_zaxira,
}
QULFSIZ = {"ai_ajrat": api_ai_ajrat}  # uzoq AI chaqiruvi — bot siklini to'xtatmasin


# =====================  Rasm proksi  =====================

_RASM_KESH = {}
_RASM_QULF = threading.Lock()


def rasm_ol(fid):
    with _RASM_QULF:
        if fid in _RASM_KESH:
            return _RASM_KESH[fid]
    kesh_papka = os.path.join(core.DATA_DIR, "rasm_kesh")
    yol = os.path.join(kesh_papka, hashlib.sha1(fid.encode()).hexdigest() + ".jpg")
    if os.path.exists(yol):
        with open(yol, "rb") as f:
            b = f.read()
    else:
        r = core.api("getFile", file_id=fid)
        if not r or not r.get("ok"):
            return None
        url = "https://api.telegram.org/file/bot" + TOKEN + "/" + r["result"]["file_path"]
        with urllib.request.urlopen(url, timeout=60, context=SSL_CTX) as f:
            b = f.read()
        try:
            os.makedirs(kesh_papka, exist_ok=True)
            with open(yol, "wb") as f:
                f.write(b)
        except Exception:
            pass
    with _RASM_QULF:
        if len(_RASM_KESH) > 300:
            _RASM_KESH.clear()
        _RASM_KESH[fid] = b
    return b


def _rasm_ruxsat(uid, fid):
    """Chek rasmlari — faqat egasi va adminlarga. Qolgan rasmlar (dizayn, portfolio) — hammaga."""
    if admin_mi(uid):
        return True
    for b in DATA["buyurtmalar"].values():
        for k in ("chek_oldindan", "chek_qolgan"):
            if b["tolov"].get(k) == fid:
                return str(b["mijoz"]) == str(uid)
    for s in DATA["sotuvlar"].values():
        if s.get("chek") == fid:
            return str(s["mijoz"]) == str(uid)
    return True


# =====================  HTTP  =====================

class Ishlovchi(BaseHTTPRequestHandler):
    server_version = "ChevarAI"

    def log_message(self, *a):
        pass

    def _yubor(self, kod, tana, tur="application/json; charset=utf-8", kesh=None):
        self.send_response(kod)
        self.send_header("Content-Type", tur)
        self.send_header("Content-Length", str(len(tana)))
        self.send_header("X-Content-Type-Options", "nosniff")
        if kesh:
            self.send_header("Cache-Control", kesh)
        self.end_headers()
        self.wfile.write(tana)

    def _json(self, kod, obj):
        self._yubor(kod, json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == "/salomatlik":
            return self._json(200, {"ok": True})
        if url.path == "/rasm":
            q = urllib.parse.parse_qs(url.query)
            fid, uid = (q.get("f") or [""])[0], token_uid((q.get("t") or [""])[0])
            if not uid or not fid or not _rasm_ruxsat(uid, fid):
                return self._json(403, {"xato": "ruxsat yo'q"})
            try:
                b = rasm_ol(fid)
            except Exception:
                b = None
            if not b:
                return self._json(404, {"xato": "rasm topilmadi"})
            return self._yubor(200, b, "image/jpeg", "private, max-age=86400")
        nom = "index.html" if url.path in ("/", "/index.html") else url.path.lstrip("/")
        yol = os.path.normpath(os.path.join(PAPKA, nom))
        if not yol.startswith(PAPKA) or not os.path.isfile(yol):
            return self._json(404, {"xato": "topilmadi"})
        with open(yol, "rb") as f:
            tana = f.read()
        tur = mimetypes.guess_type(yol)[0] or "application/octet-stream"
        if tur.startswith("text/") or tur.endswith("javascript"):
            tur += "; charset=utf-8"
        self._yubor(200, tana, tur, "no-cache")

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        if not url.path.startswith("/api/"):
            return self._json(404, {"xato": "topilmadi"})
        yol = url.path[5:]
        try:
            uzunlik = int(self.headers.get("Content-Length") or 0)
            if uzunlik > 12 * 1024 * 1024:
                raise Xato("So'rov juda katta", 413)
            d = json.loads(self.rfile.read(uzunlik) or b"{}")
            if yol == "kirish":
                user = initdata_tekshir(d.get("initData") or "")
                if not user and os.getenv("ILOVA_DEV") == "1" and d.get("dev_uid"):
                    user = {"id": int(d["dev_uid"]), "first_name": "Sinov"}
                if not user or not user.get("id"):
                    raise Xato("Telegram orqali oching", 401)
                uid = int(user["id"])
                d["_user"] = user
                with QULF:
                    if profil(uid).get("bloklangan"):
                        raise Xato("Kirish cheklangan", 403)
                    return self._json(200, api_kirish(uid, d, token_ber(uid)))
            token = self.headers.get("X-Token") or ""
            uid = token_uid(token)
            if not uid:
                raise Xato("Sessiya tugagan — ilovani qayta oching", 401)
            if yol in QULFSIZ:
                return self._json(200, QULFSIZ[yol](uid, d, token))
            fn = YOLLAR.get(yol)
            if not fn:
                raise Xato("Noma'lum so'rov", 404)
            with QULF:
                if DATA["foydalanuvchilar"].get(str(uid), {}).get("bloklangan"):
                    raise Xato("Kirish cheklangan", 403)
                return self._json(200, fn(uid, d, token))
        except Xato as e:
            return self._json(e.kod, {"xato": str(e)})
        except Exception:
            log("Ilova xatosi (" + yol + "):\n" + traceback.format_exc())
            return self._json(500, {"xato": "Ichki xato, qayta urinib ko'ring"})


def ishga_tushir():
    port = int(os.getenv("PORT") or 8080)
    server = ThreadingHTTPServer(("0.0.0.0", port), Ishlovchi)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    log("Ilova serveri: port " + str(port))
    url = os.getenv("WEBAPP_URL") or core.CFG.get("webapp_url")
    if url:
        core.api("setChatMenuButton", menu_button={"type": "web_app", "text": "📱 Ilova",
                                                   "web_app": {"url": url}})
    return server
