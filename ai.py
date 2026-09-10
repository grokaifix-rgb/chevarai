# -*- coding: utf-8 -*-
"""
Chevar AI — "aql" qismi.
Mijozning oddiy tildagi gapini hunarmand tushunadigan aniq buyurtmaga aylantiradi.

Ikki rejimda ishlaydi:
  1) AI kalit bor  -> Gemini / OpenAI-mos / Claude API orqali (config.json: ai_provider)
  2) AI kalit yo'q -> ichki "aqlli" tahlil (kalit so'zlar lug'ati) — internetsiz, tekin

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

import json
import re
import ssl
import urllib.error
import urllib.request

# =====================  Buyurtma maydonlari  =====================

MAYDONLAR = [
    ("kiyim", "Qanday kiyim kerak? (ko'ylak, chapan, kostyum, yaktak, do'ppi...)"),
    ("mato", "Qaysi matodan tikilsin? (adras, atlas, shoyi, baxmal, ipak, chit...)"),
    ("rang", "Qanday rangda bo'lsin?"),
    ("fason", "Fason qanday bo'lsin? (zamonaviy, milliy, klassik, erkin...)"),
    ("tadbir", "Qaysi tadbir uchun? (to'y, nikoh, bayram, kundalik, ish...)"),
]

QOSHIMCHA = [
    ("uzunlik", "Uzunligi qanday bo'lsin? (uzun / o'rta / kalta)"),
    ("yeng", "Yengi qanday bo'lsin? (uzun yeng / kalta yeng / yengsiz)"),
]

# =====================  Kalit so'zlar lug'ati  =====================

KIYIM_SOZLAR = {
    "ko'ylak": ["ko'ylak", "koylak", "kuylak", "платье", "dress"],
    "chapan": ["chapan", "to'n", "ton ", "khalat", "xalat"],
    "yaktak": ["yaktak", "yakhtak"],
    "kostyum": ["kostyum", "kostum", "kastyum", "pidjak", "костюм", "suit"],
    "shim": ["shim", "shalvar", "lozim", "брюки"],
    "ko'ylak-lozim": ["ko'ylak-lozim", "koylak lozim", "lozim bilan"],
    "do'ppi": ["do'ppi", "doppi", "duppi", "tubeteyka"],
    "ro'mol": ["ro'mol", "romol", "durra", "sharf", "платок"],
    "kamzul": ["kamzul", "kamzol", "jilet"],
    "etak": ["etak", "yubka", "юбка", "skirt"],
    "bluzka": ["bluzka", "kofta", "блузка"],
}

MATO_SOZLAR = {
    "adras": ["adras", "адрас"],
    "atlas": ["atlas", "xonatlas", "hon atlas", "атлас"],
    "shoyi": ["shoyi", "shohi", "shoxi", "шойи"],
    "ipak": ["ipak", "shelk", "шелк", "silk"],
    "baxmal": ["baxmal", "bahmal", "barxit", "бархат", "velvet"],
    "chit": ["chit", "ситец"],
    "shtapel": ["shtapel", "shtapil", "штапель"],
    "jinsi": ["jinsi", "denim", "джинс"],
    "gabardin": ["gabardin", "габардин"],
    "krep": ["krep", "kreppp", "креп"],
    "trikotaj": ["trikotaj", "трикотаж"],
    "kashta": ["kashta", "kashtali", "suzana", "so'zana"],
}

RANG_SOZLAR = {
    "ko'k": ["ko'k", "kok ", " kuk", "moviy", "синий", "blue"],
    "qizil": ["qizil", "красн", "red"],
    "yashil": ["yashil", "зелён", "зелен", "green"],
    "sariq": ["sariq", "жёлт", "желт", "yellow"],
    "oq": ["oq ", " oq", "oq-", "белый", "white"],
    "qora": ["qora", "чёрн", "черн", "black"],
    "pushti": ["pushti", "розов", "pink"],
    "bordo": ["bordo", "бордо"],
    "bejeviy": ["bej", "беж"],
    "kulrang": ["kulrang", "seriy", "сер", "gray", "grey"],
    "oltin": ["oltin", "tilla", "золот", "gold"],
    "binafsha": ["binafsha", "siren", "фиолет", "purple"],
}

FASON_SOZLAR = {
    "zamonaviy": ["zamonaviy", "modern", "hozirgi zamon", "стильн", "современ"],
    "milliy": ["milliy", "an'anaviy", "ananaviy", "milly", "национал"],
    "klassik": ["klassik", "классик", "classic"],
    "erkin": ["erkin", "keng", "oversize", "свободн"],
    "tor": ["tor ", "yopishgan", "приталенн", "slim"],
}

TADBIR_SOZLAR = {
    "to'y": ["to'y", "toy ", "tuy", "nikoh", "kelin", "свадьб", "wedding"],
    "bayram": ["bayram", "navro'z", "navruz", "hayit", "праздник"],
    "kundalik": ["kundalik", "har kuni", "oddiy kiyim", "повседнев"],
    "ish": ["ish uchun", "ofis", "офис", "work"],
    "sovg'a": ["sovg'a", "sovga", "подарок", "gift"],
}

UZUNLIK_SOZLAR = {
    "uzun": ["uzun", "maxi", "длинн"],
    "o'rta": ["o'rta", "orta", "midi", "средн"],
    "kalta": ["kalta", "qisqa", "mini", "коротк"],
}

YENG_SOZLAR = {
    "uzun yeng": ["uzun yeng", "uzun yengli", "длинный рукав"],
    "kalta yeng": ["kalta yeng", "qisqa yeng", "короткий рукав"],
    "yengsiz": ["yengsiz", "yeng yo'q", "без рукав"],
}


def _topish(matn, lugat):
    """Matndan lug'atdagi so'zlarni topadi, topilganini qaytaradi."""
    past = " " + matn.lower().replace("’", "'").replace("`", "'") + " "
    topilgan = []
    for nom, sozlar in lugat.items():
        for s in sozlar:
            if s in past:
                topilgan.append(nom)
                break
    return topilgan


# =====================  Offline (kalitsiz) tahlil  =====================

def offline_tahlil(matnlar):
    """
    Internetsiz/kalitsiz rejim: mijoz yozgan barcha gaplardan buyurtma yig'adi.
    matnlar — mijozning shu suhbatdagi barcha xabarlari ro'yxati.
    """
    hammasi = "\n".join(matnlar)
    buyurtma = {}

    kiyim = _topish(hammasi, KIYIM_SOZLAR)
    if kiyim:
        buyurtma["kiyim"] = kiyim[0]

    mato = _topish(hammasi, MATO_SOZLAR)
    if mato:
        buyurtma["mato"] = ", ".join(mato[:2])

    rang = _topish(hammasi, RANG_SOZLAR)
    if rang:
        buyurtma["rang"] = "-".join(rang[:2])

    fason = _topish(hammasi, FASON_SOZLAR)
    if fason:
        buyurtma["fason"] = fason[0]

    tadbir = _topish(hammasi, TADBIR_SOZLAR)
    if tadbir:
        buyurtma["tadbir"] = tadbir[0]

    uz = _topish(hammasi, UZUNLIK_SOZLAR)
    if uz:
        buyurtma["uzunlik"] = uz[0]

    yeng = _topish(hammasi, YENG_SOZLAR)
    if yeng:
        buyurtma["yeng"] = yeng[0]

    buyurtma["izoh"] = matnlar[0][:300] if matnlar else ""

    # Yetishmayotgan asosiy maydon uchun savol
    for kalit, savol in MAYDONLAR:
        if not buyurtma.get(kalit):
            return {"tayyor": False, "savol": savol, "buyurtma": buyurtma}

    return {"tayyor": True, "savol": None, "buyurtma": buyurtma}


# =====================  AI (kalit bilan) tahlil  =====================

TIZIM_PROMPT = """Sen — "Chevar AI" nomli o'zbek tikuvchilik platformasining buyurtma qabul qiluvchisisan.
Mijoz oddiy tilda kiyim buyurtmasini yozadi. Sening vazifang — uni hunarmand (tikuvchi) tushunadigan
aniq texnik buyurtmaga aylantirish.

QOIDALAR:
- Faqat o'zbek tilida, iliq va sodda gapir. Mijoz dasturchi emas.
- Bir vaqtda FAQAT BITTA savol ber, qisqa qilib.
- Quyidagilar ma'lum bo'lsa yetarli: kiyim turi, mato, rang, fason, tadbir.
- Agar shular ma'lum bo'lsa — savol berma, buyurtmani tayyor deb belgila.
- O'lcham va muddat haqida SO'RAMA — ularni tizimning o'zi keyin so'raydi.
- Mato/rang haqida bilimdon maslahat berishing mumkin (masalan: to'yga adras yoki atlas mos keladi).

JAVOBNI FAQAT JSON ko'rinishida ber, boshqa hech narsa yozma:
{"tayyor": true/false, "savol": "mijozga beriladigan bitta savol yoki null",
 "buyurtma": {"kiyim":"", "mato":"", "rang":"", "fason":"", "tadbir":"",
              "uzunlik":"", "yeng":"", "bezak":"", "izoh":""}}
"""


def _ssl_ctx():
    ctx = ssl.create_default_context()
    if ssl.get_default_verify_paths().cafile is None:
        try:
            import certifi
            ctx = ssl.create_default_context(cafile=certifi.where())
        except Exception:
            for p in ("/etc/ssl/cert.pem", "/private/etc/ssl/cert.pem"):
                import os
                if os.path.exists(p):
                    ctx = ssl.create_default_context(cafile=p)
                    break
    return ctx


def _post(url, data, headers, timeout=45):
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx()) as r:
        return json.loads(r.read().decode("utf-8"))


def _json_ajrat(matn):
    """AI javobidan JSON qismini ajratib oladi."""
    matn = matn.strip()
    matn = re.sub(r"^```(json)?", "", matn).strip()
    matn = re.sub(r"```$", "", matn).strip()
    boshi = matn.find("{")
    oxiri = matn.rfind("}")
    if boshi == -1 or oxiri == -1:
        raise ValueError("JSON topilmadi")
    return json.loads(matn[boshi:oxiri + 1])


def ai_tahlil(cfg, suhbat):
    """
    suhbat — [{"rol": "mijoz"/"ai", "matn": "..."}] ko'rinishidagi ro'yxat.
    Xatolik bo'lsa Exception ko'taradi (chaqiruvchi offline rejimga o'tadi).
    """
    provider = (cfg.get("ai_provider") or "yoq").lower()
    key = cfg.get("ai_key") or ""
    model = cfg.get("ai_model") or ""

    if provider in ("yoq", "", "offline"):
        raise ValueError("AI o'chirilgan")
    if not key:
        raise ValueError("AI kalit yo'q")

    if provider == "gemini":
        model = model or "gemini-3.6-flash"
        url = ("https://generativelanguage.googleapis.com/v1beta/models/"
               + model + ":generateContent?key=" + key)
        parts = []
        for x in suhbat:
            rol = "user" if x["rol"] == "mijoz" else "model"
            parts.append({"role": rol, "parts": [{"text": x["matn"]}]})
        body = {
            "systemInstruction": {"parts": [{"text": TIZIM_PROMPT}]},
            "contents": parts,
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 2000,
                                 "responseMimeType": "application/json"},
        }
        j = _post(url, body, {"Content-Type": "application/json"})
        bolaklar = j["candidates"][0]["content"].get("parts") or []
        matn = "".join(b.get("text", "") for b in bolaklar)

    elif provider == "claude":
        model = model or "claude-sonnet-5"
        msgs = [{"role": ("user" if x["rol"] == "mijoz" else "assistant"),
                 "content": x["matn"]} for x in suhbat]
        body = {"model": model, "max_tokens": 800, "system": TIZIM_PROMPT,
                "messages": msgs}
        j = _post("https://api.anthropic.com/v1/messages", body, {
            "Content-Type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        })
        matn = j["content"][0]["text"]

    else:  # openai va unga mos servislar (Groq, OpenRouter, ...)
        model = model or "gpt-4o-mini"
        base = cfg.get("ai_url") or "https://api.openai.com/v1/chat/completions"
        msgs = [{"role": "system", "content": TIZIM_PROMPT}]
        for x in suhbat:
            msgs.append({"role": ("user" if x["rol"] == "mijoz" else "assistant"),
                         "content": x["matn"]})
        body = {"model": model, "messages": msgs, "temperature": 0.4}
        j = _post(base, body, {"Content-Type": "application/json",
                               "Authorization": "Bearer " + key})
        matn = j["choices"][0]["message"]["content"]

    natija = _json_ajrat(matn)
    natija.setdefault("tayyor", False)
    natija.setdefault("savol", None)
    natija.setdefault("buyurtma", {})
    return natija


def tahlil(cfg, suhbat):
    """Asosiy kirish nuqtasi: avval AI, xato bo'lsa offline tahlil."""
    try:
        return ai_tahlil(cfg, suhbat)
    except Exception:
        matnlar = [x["matn"] for x in suhbat if x["rol"] == "mijoz"]
        return offline_tahlil(matnlar)


# =====================  Buyurtma varaqasi  =====================

NOM = {
    "kiyim": "Kiyim turi", "mato": "Mato", "rang": "Rang", "fason": "Fason",
    "tadbir": "Vazifa", "uzunlik": "Uzunlik", "yeng": "Yeng",
    "bezak": "Bezak", "izoh": "Mijoz izohi",
}
TARTIB = ["kiyim", "mato", "rang", "fason", "tadbir", "uzunlik", "yeng", "bezak", "izoh"]


def varaqa(buyurtma):
    """Buyurtmani chiroyli matn ko'rinishiga keltiradi."""
    qatorlar = []
    for k in TARTIB:
        qiymat = (buyurtma.get(k) or "").strip()
        if qiymat:
            qatorlar.append("• <b>" + NOM[k] + ":</b> " + qiymat)
    return "\n".join(qatorlar) if qatorlar else "• (ma'lumot yo'q)"
