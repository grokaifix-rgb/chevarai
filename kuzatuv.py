# -*- coding: utf-8 -*-
"""
Chevar AI — buyurtmani kuzatish va hunarmand sharhlari.

Tikish buyurtmasi bosqichlari (mijoz har birini ko'rib turadi):
  📥 Qabul qilindi → 🪡 Tikilmoqda → 🎊 Tayyor → 🚚 Yetkazilmoqda → ✅ Topshirildi

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

from core import DATA, esc, profil, saqla, vaqt

BOSQICHLAR = [
    ("yuborildi", "📤 Hunarmandga yuborildi"),
    ("kelishilmoqda", "💬 Narx va muddat kelishilmoqda"),
    ("tasdiqlandi", "✅ Tasdiqlandi"),
    ("tikilmoqda", "🪡 Tikilmoqda"),
    ("tayyor", "🎊 Tayyor"),
    ("yetkazilmoqda", "🚚 Yetkazilmoqda"),
    ("yakunlandi", "📦 Yetkazildi"),
]
_INDEKS = {"yangi": 0, "tasdiqlangan": 2, "tikilmoqda": 3, "tayyor": 4,
           "yetkazilmoqda": 5, "yakunlandi": 6}


def _joriy(b):
    i = _INDEKS.get(b.get("holat"), 0)
    if b.get("holat") == "yangi" and b.get("takliflar"):
        i = 1
    return i


HOLAT_NOMI = {
    "tasdiqlangan": "✅ Tasdiqlandi — oldindan to'lov kutilmoqda",
    "tikilmoqda": "🪡 Tikilmoqda",
    "tayyor": "🎊 Tayyor — yakuniy to'lov",
    "yetkazilmoqda": "🚚 Yetkazilmoqda",
    "yakunlandi": "📦 Yetkazildi",
    "bekor": "❌ Bekor qilindi",
}


def holat_nomi(b):
    """Texnik topshiriqdagi holat nomlari."""
    if b.get("holat") == "yangi":
        if b.get("takliflar"):
            return "💬 Narx va muddat kelishilmoqda (" + str(len(b["takliflar"])) + " ta taklif)"
        if b.get("korilmoqda"):
            return "👀 Hunarmand ko'rib chiqmoqda"
        return "📤 Hunarmandga yuborildi"
    return HOLAT_NOMI.get(b.get("holat"), b.get("holat"))


def belgila(b, bosqich):
    """Bosqichga o'tgan vaqtni yozib qo'yadi (bir marta)."""
    b.setdefault("vaqtlar", {}).setdefault(bosqich, vaqt())


def matn(b):
    """Buyurtma bosqichlari ro'yxati: o'tganlari ✅, hozirgisi 👉, keyingilari ▫️."""
    if b.get("holat") == "bekor":
        return "❌ Buyurtma bekor qilingan"
    joriy = _joriy(b)
    vaqtlar = dict(b.get("vaqtlar", {}))
    vaqtlar.setdefault("yuborildi", vaqtlar.get("qabul") or b.get("yaratildi", ""))
    q = []
    for i, (kalit, nom) in enumerate(BOSQICHLAR):
        sana = vaqtlar.get(kalit, "")
        if i < joriy or (i == joriy == len(BOSQICHLAR) - 1):
            q.append("✅ " + nom[2:].strip() + ("  <i>" + sana + "</i>" if sana else ""))
        elif i == joriy:
            q.append("👉 <b>" + nom + "</b>" + ("  <i>" + sana + "</i>" if sana else ""))
        else:
            q.append("▫️ " + nom[2:].strip())
    if b.get("holat") == "yangi":
        q.append("\n<i>" + holat_nomi(b) + "</i>")
    elif b.get("holat") == "tasdiqlangan":
        q.append("\n<i>Oldindan to'lov kutilmoqda</i>")
    elif b.get("holat") == "tikilmoqda" and b.get("muddat_kun"):
        q.append("\n<i>Usta muddati: " + str(b["muddat_kun"]) + " kun</i>")
    return "\n".join(q)


def kuzatish_kartasi(b):
    tur = esc((b.get("tafsilot") or {}).get("kiyim") or "buyurtma")
    return ("📍 <b>Buyurtma #" + b["raqam"] + "</b> — " + tur + "\n\n" + matn(b))


# =====================  Sharhlar  =====================

def sharh_qosh(usta_uid, b, ball, matn_=""):
    p = profil(usta_uid)
    mijoz = DATA["foydalanuvchilar"].get(str(b["mijoz"]), {})
    ism = (mijoz.get("ism") or "Mijoz").split()[0]
    p.setdefault("sharhlar", []).append({
        "baho": int(ball), "matn": matn_[:400], "mijoz": ism,
        "raqam": b["raqam"], "sana": vaqt()[:10],
        "kiyim": (b.get("tafsilot") or {}).get("kiyim", ""),
    })
    saqla()


def sharhlar_matni(usta_uid, n=2):
    """Oxirgi n ta matnli sharh (taklif ichida ko'rsatish uchun)."""
    sh = [s for s in DATA["foydalanuvchilar"].get(str(usta_uid), {}).get("sharhlar", []) if s.get("matn")]
    if not sh:
        return ""
    q = []
    for s in sh[-n:][::-1]:
        q.append("«" + s["matn"][:120] + "» — " + s["mijoz"] + ", " + "⭐️" * s["baho"])
    return "💬 " + "\n💬 ".join(q)


def barcha_sharhlar(usta_uid):
    p = DATA["foydalanuvchilar"].get(str(usta_uid), {})
    sh = p.get("sharhlar", [])
    if not sh:
        return "Bu hunarmandga hali sharh yozilmagan."
    q = ["💬 <b>" + esc(p.get("ism") or "Hunarmand") + " haqida sharhlar</b> (" + str(len(sh)) + ")\n"]
    for s in sh[::-1][:15]:
        q.append("⭐️" * s["baho"] + "  <i>" + s["sana"] + "</i> — " + s["mijoz"]
                 + (" · " + esc(s["kiyim"]) if s.get("kiyim") else "")
                 + ("\n«" + s["matn"] + "»" if s.get("matn") else "") + "\n")
    return "\n".join(q)
