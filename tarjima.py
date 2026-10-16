# -*- coding: utf-8 -*-
"""
Chevar AI — ko'p tillilik: o'zbek (asosiy), ingliz, qoraqalpoq.

Ishlash tartibi:
  1) Menyu tugmalari va asosiy iboralar — qo'lda yozilgan lug'at (LUGAT).
     Pastdagi menyu tugmalari faqat shu lug'atdan olinadi, chunki foydalanuvchi
     bosgan tugma matni orqali bot qaysi tugma bosilganini taniydi.
  2) Qolgan xabarlar — Gemini orqali tarjima qilinadi va keshga yoziladi
     (bir marta tarjima qilingan matn qayta so'ralmaydi).
  3) AI ishlamasa — xabar o'zbekcha yuboriladi, bot to'xtamaydi.

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

import json
import os
import re
import threading

TILLAR = {
    "uz": "🇺🇿 O'zbekcha",
    "kaa": "🏳️ Qaraqalpaqsha",
    "en": "🇬🇧 English",
}
TIL_NOMI_AI = {"en": "English", "kaa": "Karakalpak (Latin script, e.g. á, ó, ú, ı, ń, ǵ)"}

# Qo'lda tarjima qilingan tugmalar va qisqa iboralar: uz -> {kaa, en}
LUGAT = {
    # --- mijoz menyusi
    "🤖 AI bilan buyurtma": {"kaa": "🤖 AI menen buyırtpa", "en": "🤖 Order with AI"},
    "👗 Dizaynlar": {"kaa": "👗 Dizaynlar", "en": "👗 Designs"},
    "🛍 Do'kon": {"kaa": "🛍 Dúkan", "en": "🛍 Shop"},
    "🛒 Savatim": {"kaa": "🛒 Sebetim", "en": "🛒 My cart"},
    "📦 Buyurtmalarim": {"kaa": "📦 Buyırtpalarım", "en": "📦 My orders"},
    "ℹ️ Yordam": {"kaa": "ℹ️ Járdem", "en": "ℹ️ Help"},
    "🪡 Men hunarmandman": {"kaa": "🪡 Men sheberman", "en": "🪡 I am an artisan"},
    "🌐 Til": {"kaa": "🌐 Til", "en": "🌐 Language"},
    # --- hunarmand menyusi
    "📋 Yangi buyurtmalar": {"kaa": "📋 Jańa buyırtpalar", "en": "📋 New orders"},
    "🧾 Mening ishlarim": {"kaa": "🧾 Meniń jumıslarım", "en": "🧾 My jobs"},
    "👤 Profilim": {"kaa": "👤 Profilim", "en": "👤 My profile"},
    "🖼 Portfolio": {"kaa": "🖼 Portfolio", "en": "🖼 Portfolio"},
    "⏸ Dam olish": {"kaa": "⏸ Dem alıw", "en": "⏸ Take a break"},
    # --- admin menyusi
    "📊 Statistika": {"kaa": "📊 Statistika", "en": "📊 Statistics"},
    "🤖 Tikish buyurtmalari": {"kaa": "🤖 Tigiw buyırtpaları", "en": "🤖 Tailoring orders"},
    "🛍 Do'kon buyurtmalari": {"kaa": "🛍 Dúkan buyırtpaları", "en": "🛍 Shop orders"},
    "🛒 Mahsulot qo'shish": {"kaa": "🛒 Ónim qosıw", "en": "🛒 Add product"},
    "👗 Dizayn qo'shish": {"kaa": "👗 Dizayn qosıw", "en": "👗 Add design"},
    "🪡 Hunarmandlar": {"kaa": "🪡 Sheberler", "en": "🪡 Artisans"},
    "👥 Foydalanuvchilar": {"kaa": "👥 Paydalanıwshılar", "en": "👥 Users"},
    "📋 Ro'yxat": {"kaa": "📋 Dizim", "en": "📋 Catalog list"},
    "👤 Mijoz rejimiga o'tish": {"kaa": "👤 Klient rejimine ótiw", "en": "👤 Switch to customer view"},
    "🛠 Admin panelga qaytish": {"kaa": "🛠 Admin panelge qaytıw", "en": "🛠 Back to admin panel"},
}

# Teskari lug'at: istalgan tildagi tugma matni -> o'zbekcha asl matn
TESKARI = {}
for _uz, _tr in LUGAT.items():
    for _t in _tr.values():
        TESKARI[_t] = _uz


def asl_tugma(matn):
    """Foydalanuvchi bosgan tarjima qilingan tugma matnini o'zbekchaga qaytaradi."""
    return TESKARI.get(matn, matn)


# =====================  Kesh  =====================

_qulf = threading.Lock()
_KESH = None
_KESH_MAX = 4000  # har til uchun


def _kesh_fayli():
    from core import DATA_DIR
    return os.path.join(DATA_DIR, "tarjima.json")


def _kesh():
    """Kesh = loyihadagi tayyor tarjimalar (tarjima_tayyor.json) + serverda yig'ilganlari."""
    global _KESH
    if _KESH is None:
        _KESH = {"en": {}, "kaa": {}}
        tayyor = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tarjima_tayyor.json")
        for yol in (tayyor, _kesh_fayli()):
            try:
                with open(yol, "r", encoding="utf-8") as f:
                    for til, d in json.load(f).items():
                        _KESH.setdefault(til, {}).update(d)
            except Exception:
                pass
    return _KESH


def _kesh_saqla():
    try:
        k = _kesh()
        for til in k:
            if len(k[til]) > _KESH_MAX:
                for eski in list(k[til])[:len(k[til]) - _KESH_MAX]:
                    del k[til][eski]
        tmp = _kesh_fayli() + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(k, f, ensure_ascii=False)
        os.replace(tmp, _kesh_fayli())
    except Exception:
        pass


# =====================  Qolip (raqamlar o'rniga belgi)  =====================
# "Buyurtma #1001 — 770 000 so'm" -> "Buyurtma #⟦0⟧ — ⟦1⟧ so'm": bir xil qolip bir marta
# tarjima qilinadi, raqamlar keyin joyiga qo'yiladi.

_RAQAM = re.compile(r"\+?\d[\d ]*\d|\d")


def _qolip(qator):
    raqamlar = []

    def _almash(m):
        raqamlar.append(m.group(0))
        return "⟦" + str(len(raqamlar) - 1) + "⟧"
    return _RAQAM.sub(_almash, qator), raqamlar


def _toldir(qolip, raqamlar):
    for i, r in enumerate(raqamlar):
        qolip = qolip.replace("⟦" + str(i) + "⟧", r)
    return qolip


def _yaroqli(asl, tr):
    """Tarjimada barcha ⟦n⟧ belgilar saqlanganmi."""
    return all(t in tr for t in re.findall(r"⟦\d+⟧", asl))


# =====================  AI tarjima  =====================

TARJIMA_MODELI = "gemini-3.5-flash-lite"   # buyurtma suhbatining limitini yemasligi uchun


def _ai_tarjima(matnlar, til, model=None):
    import ai
    from core import AI_CFG
    prompt = (
        "Translate each Uzbek string in the JSON array into " + TIL_NOMI_AI[til] + ".\n"
        "Rules: keep HTML tags (<b>, <i>, <code>, <a href=...>) exactly; keep emojis, "
        "placeholders like ⟦0⟧ ⟦1⟧ (exactly, do not translate or remove them), #order numbers, "
        "@usernames, /commands unchanged; keep people's names unchanged. 'so'm' is the Uzbek "
        "currency (English: 'UZS', Karakalpak: 'swm'). Fabric names: adras, atlas, shoyi stay as is "
        "(in English you may add 'ikat' in brackets once). This is a Telegram bot of a tailoring "
        "marketplace: keep it short, warm and natural. If a string is already in the target "
        "language, return it unchanged.\n"
        "Return ONLY a JSON array of translated strings, same length and order.\n\n"
        + json.dumps(matnlar, ensure_ascii=False)
    )
    javob = ai.erkin_soro(AI_CFG, prompt, model or TARJIMA_MODELI)
    natija = json.loads(javob[javob.find("["): javob.rfind("]") + 1])
    if not isinstance(natija, list) or len(natija) != len(matnlar):
        raise ValueError("tarjima uzunligi mos emas")
    return [str(x) for x in natija]


def tarjima(matnlar, til):
    """Matnlar ro'yxatini tarjima qiladi (qatorma-qator, qolip bilan).
    Tarjima topilmagan qator o'zbekcha qoladi — bot hech qachon to'xtamaydi."""
    if til not in TIL_NOMI_AI or not matnlar:
        return list(matnlar)
    k = _kesh().setdefault(til, {})

    # 1) Har bir matnni qatorlarga, har qatorni qolipga ajratamiz
    tuzilma = []
    kerak = []
    for m in matnlar:
        if m in LUGAT:
            tuzilma.append(("lugat", LUGAT[m][til]))
            continue
        qatorlar = []
        for q in (m or "").split("\n"):
            if not re.search(r"[A-Za-zА-Яа-я]", q):
                qatorlar.append(("tayyor", q))
                continue
            qolip, raqamlar = _qolip(q)
            qatorlar.append(("qolip", qolip, raqamlar))
            if qolip not in k and qolip not in kerak:
                kerak.append(qolip)
        tuzilma.append(("qatorlar", qatorlar))

    # 2) Keshda yo'q qoliplarni bitta so'rovda tarjima qilamiz
    if kerak:
        try:
            tarjimalar = _ai_tarjima(kerak, til)
            with _qulf:
                for asl, tr in zip(kerak, tarjimalar):
                    if _yaroqli(asl, tr):
                        k[asl] = tr
                _kesh_saqla()
        except Exception:
            pass

    # 3) Yig'amiz
    natija = []
    for t in tuzilma:
        if t[0] == "lugat":
            natija.append(t[1])
            continue
        qismlar = []
        for q in t[1]:
            if q[0] == "tayyor":
                qismlar.append(q[1])
            else:
                qismlar.append(_toldir(k.get(q[1], q[1]), q[2]))
        natija.append("\n".join(qismlar))
    return natija


def til_tugmalari():
    return {"inline_keyboard": [[{"text": nom, "callback_data": "til_" + kod}]
                                for kod, nom in TILLAR.items()]}
