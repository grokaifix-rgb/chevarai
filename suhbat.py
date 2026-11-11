# -*- coding: utf-8 -*-
"""
Chevar AI — mahsulot turiga mos buyurtma suhbati (texnik topshiriq 3–6-bo'limlar).

Qoidalar:
  • avval mahsulot turi aniqlanadi (ko'ylak, sumka, yubka, nimcha, kashtachilik, aksessuar, boshqa);
  • har tur uchun faqat o'z savollari beriladi (sumkaga bo'y/yeng so'ralmaydi);
  • berilgan javoblar saqlanadi va qayta so'ralmaydi, faqat yetishmagani so'raladi;
  • «boshqa rang», «ko'ylak emas, sumka», «oldingi javobni o'zgartir», «bekor qil»,
    «tikuvchi bilan gaplashmoqchiman» kabi gaplar tushuniladi;
  • narx va muddat uydirilmaydi — ularni hunarmand taklif qiladi.

Qaysi savol berilishini KOD hal qiladi (bir xil va sinab bo'ladigan), AI esa faqat
mijozning erkin gapidan qiymatlarni ajratib oladi. AI ishlamasa — kalit so'zlar va
«oxirgi so'ralgan maydonga javob» qoidasi bilan ishlaydi.

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

import json
import re

import alifbo

# ---------------------------------------------------------------- turlar
# maydon: (nomi, savol)
TURLAR = {
    "ko'ylak": {
        "nom": "Ko'ylak / kiyim",
        "maydonlar": [
            ("mato", "Qaysi matodan bo'lsin? (adras, atlas, shoyi, baxmal, chit...)"),
            ("rang", "Qanday rangda bo'lsin?"),
            ("fason", "Fasoni qanday bo'lsin? (milliy, zamonaviy, klassik, erkin...)"),
            ("uzunlik", "Uzunligi qanday bo'lsin? (uzun, o'rta yoki kalta)"),
            ("yeng", "Yengi qanday bo'lsin? (uzun, kalta yoki yengsiz)"),
            ("yoqa", "Yoqasi qanday bo'lsin? (tik yoqa, aylana, V-shakl, yoqasiz...)"),
            ("tadbir", "Qaysi tadbir uchun? (to'y, bayram, kundalik, ish...)"),
        ],
        "olcham": ["boy", "kokrak", "bel", "son"],
    },
    "sumka": {
        "nom": "Sumka",
        "maydonlar": [
            ("material", "Qaysi materialdan bo'lsin? (adras, atlas, baxmal, charm, jinsi...)"),
            ("rang", "Qanday rangda bo'lsin?"),
            ("hajm", "Hajmi kichik, o'rtacha yoki katta bo'lsin?"),
            ("shakl", "Shakli qanday bo'lsin? (to'rtburchak, dumaloq, tugunli, xalta...)"),
            ("dastak", "Dastak: qisqa, uzun yelkaga osiladigan yoki ikkalasi ham?"),
            ("chontak", "Ichki cho'ntak kerakmi? Nechta?"),
            ("yopilish", "Fermuar, magnit yoki tugma bilan yopilsinmi?"),
            ("bezak", "Bezak kerakmi? (munchoq, popuk, kashta, yo'q)"),
        ],
        "olcham": [],
    },
    "yubka": {
        "nom": "Yubka",
        "maydonlar": [
            ("mato", "Qaysi matodan bo'lsin?"),
            ("rang", "Qanday rangda bo'lsin?"),
            ("fason", "Fasoni qanday bo'lsin? (to'g'ri, burmali, qo'ng'iroq, plise...)"),
            ("uzunlik", "Uzunligi qanday bo'lsin? (uzun, o'rta yoki kalta)"),
            ("astar", "Astar kerakmi?"),
        ],
        "olcham": ["bel", "son"],
    },
    "nimcha": {
        "nom": "Nimcha",
        "maydonlar": [
            ("mato", "Qaysi matodan bo'lsin? (adras, baxmal, jinsi, atlas...)"),
            ("rang", "Qanday rangda bo'lsin?"),
            ("fason", "Fasoni qanday bo'lsin? (milliy, zamonaviy, o'ralma, korset...)"),
            ("uzunlik", "Uzunligi qanday bo'lsin? (kalta, belgacha, uzun)"),
            ("yoqa", "Yoqasi qanday bo'lsin? (V-shakl, tik yoqa, yoqasiz...)"),
            ("yopilish", "Tugma, fermuar yoki bog'ich bilan yopilsinmi?"),
        ],
        "olcham": ["kokrak", "bel"],
    },
    "kashta": {
        "nom": "Kashtachilik",
        "maydonlar": [
            ("buyum", "Kashta qaysi buyumga tikilsin? (ko'ylak, so'zana, do'ppi, yostiq, ro'mol...)"),
            ("naqsh", "Qanday naqsh bo'lsin? (gul, qo'chqor shoxi, anor, islimiy, geometrik...)"),
            ("rang", "Kashta ranglari qanday bo'lsin?"),
            ("mato", "Qaysi mato ustiga tikiladi?"),
            ("joy", "Naqsh buyumning qayeriga tikilsin? (yoqa, yeng uchi, etak, butun yuza...)"),
            ("olchami", "Buyum yoki naqsh o'lchami qancha? (masalan: 40×60 sm)"),
        ],
        "olcham": [],
    },
    "aksessuar": {
        "nom": "Aksessuar",
        "maydonlar": [
            ("turi", "Qanday aksessuar? (do'ppi, belbog', yoqa, ro'mol, taqinchoq...)"),
            ("material", "Qaysi materialdan bo'lsin?"),
            ("rang", "Qanday rangda bo'lsin?"),
            ("dizayn", "Dizayni qanday bo'lsin? (milliy naqsh, oddiy, toshli, kashtali...)"),
            ("moslik", "O'lchami yoki kimga mos bo'lsin? (masalan: bosh aylanasi 56 sm, bola uchun)"),
        ],
        "olcham": [],
    },
    "boshqa": {
        "nom": "Boshqa mahsulot",
        "maydonlar": [("tavsif", "Qanday buyum kerakligini batafsilroq yozing.")],
        "olcham": [],
    },
}

TUR_TANLASH = "Avval aniqlab olay: nima kerak?"
TUR_TUGMALARI = [
    [("👗 Ko'ylak / kiyim", "tur_ko'ylak"), ("👜 Sumka", "tur_sumka")],
    [("🩳 Yubka", "tur_yubka"), ("🦺 Nimcha", "tur_nimcha")],
    [("🪡 Kashtachilik", "tur_kashta"), ("💍 Aksessuar", "tur_aksessuar")],
    [("❔ Boshqa", "tur_boshqa")],
]

MAYDON_NOMI = {
    "tur": "Mahsulot", "kiyim": "Kiyim", "mato": "Mato", "material": "Material", "rang": "Rang",
    "fason": "Fason", "uzunlik": "Uzunlik", "yeng": "Yeng", "yoqa": "Yoqa", "tadbir": "Tadbir",
    "hajm": "Hajm", "shakl": "Shakl", "dastak": "Dastak", "chontak": "Ichki cho'ntak",
    "yopilish": "Yopilish", "bezak": "Bezak", "astar": "Astar", "buyum": "Buyum", "naqsh": "Naqsh",
    "joy": "Naqsh joyi", "olchami": "O'lcham", "turi": "Turi", "dizayn": "Dizayn",
    "moslik": "O'lcham / moslik", "tavsif": "Tavsif", "izoh": "Qo'shimcha",
}

OLCHAM_SAVOL = {
    "boy": "📏 Bo'yingiz necha sm? (masalan: 165)",
    "kokrak": "📏 Ko'krak aylanasi necha sm? (bilmasangiz «-» yozing)",
    "bel": "📏 Bel aylanasi necha sm? (bilmasangiz «-» yozing)",
    "son": "📏 Son (dumba) aylanasi necha sm? (bilmasangiz «-» yozing)",
}
OLCHAM_NOMI = {"boy": "Bo'y", "kokrak": "Ko'krak", "bel": "Bel", "son": "Son"}

# ---------------------------------------------------------------- kalit so'zlar
TUR_SOZLAR = {
    "sumka": ["sumka", "сумка", "bag", "handbag", "xalta", "ryukzak", "hamyon", "koshelok"],
    "yubka": ["yubka", "юбка", "skirt", "etak "],
    "nimcha": ["nimcha", "нимча", "kamzul", "kamzol", "jilet", "vest", "waistcoat", "жилет"],
    "kashta": ["kashta", "кашта", "so'zana", "suzana", "embroider", "вышив", "kesteli", "kesteshilik"],
    "aksessuar": ["do'ppi", "doppi", "дўппи", "belbog'", "belbog", "ro'mol", "romol", "taqinchoq",
                  "aksessuar", "accessor", "kepka", "bilaguzuk", "sirg'a", "marjon"],
    "ko'ylak": ["ko'ylak", "koylak", "kuylak", "кўйлак", "платье", "dress", "gown", "kóylek",
                "chapan", "чапан", "to'n", "kurtka", "куртка", "jacket", "palto", "пальто", "coat",
                "kostyum", "костюм", "suit", "yaktak", "korset", "corset", "kiyim", "bluzka", "kofta",
                "shim", "lozim", "kimono", "libos"],
}

QIYMAT_SOZLAR = {
    "mato": {"adras": ["adras", "ikat"], "atlas": ["atlas", "xonatlas"], "shoyi": ["shoyi", "shohi", "silk", "ipak"],
             "baxmal": ["baxmal", "bahmal", "velvet"], "chit": ["chit"], "jinsi": ["jinsi", "denim"],
             "jun": ["jun ", "wool"], "zig'ir": ["zig'ir", "linen"], "krep": ["krep"]},
    "rang": {"ko'k": ["ko'k", " kok", "moviy", "blue"], "qizil": ["qizil", "red"], "yashil": ["yashil", "green"],
             "sariq": ["sariq", "yellow"], "oq": [" oq ", " oq,", "oq-", "white"], "qora": ["qora", "black"],
             "pushti": ["pushti", "pink"], "bordo": ["bordo"], "tillarang": ["tillarang", "oltin", "gold"],
             "firuza": ["firuza", "turquoise"], "jigarrang": ["jigarrang", "brown"],
             "rang-barang": ["rang-barang", "rangbarang", "colorful", "colourful"]},
    "fason": {"zamonaviy": ["zamonaviy", "modern"], "milliy": ["milliy", "an'anaviy", "traditional"],
              "klassik": ["klassik", "classic"], "erkin": ["erkin", "keng", "oversize"]},
    "uzunlik": {"uzun": ["uzun ", "maxi", "long"], "o'rta": ["o'rta", "midi"], "kalta": ["kalta", "qisqa", "short", "mini"]},
    "yeng": {"uzun yeng": ["uzun yeng", "long sleeve"], "kalta yeng": ["kalta yeng", "qisqa yeng", "short sleeve"],
             "yengsiz": ["yengsiz", "sleeveless"]},
    "tadbir": {"to'y": ["to'y", "toy", "nikoh", "kelin", "wedding"], "bayram": ["bayram", "navro'z", "hayit"],
               "kundalik": ["kundalik", "har kuni", "daily", "everyday"], "ish": ["ish uchun", "ofis", "office"]},
    "hajm": {"kichik": ["kichik", "small", "mini"], "o'rtacha": ["o'rtacha", "orta", "medium"],
             "katta": ["katta", "large", "big"]},
    "dastak": {"ikkala dastak": ["ikkalasi", "ikki xil", "both"], "qisqa dastak": ["qisqa dastak", "qo'lda"],
               "uzun (yelkaga)": ["yelka", "uzun dastak", "shoulder"]},
    "yopilish": {"fermuar": ["fermuar", "zamok", "zip"], "magnit": ["magnit", "magnet"],
                 "tugma": ["tugma", "button"], "bog'ich": ["bog'ich", "tie"]},
}
QIYMAT_SOZLAR["material"] = QIYMAT_SOZLAR["mato"]

TASDIQ_SOZ = ["ha", "xa", "tasdiq", "to'g'ri", "togri", "yes", "ok", "окей", "ҳа", "awa", "áwe", "maqul", "ma'qul"]
FARQI_YOQ = ["farqi yo'q", "farqi yoq", "bilmayman", "ixtiyoriy", "any", "doesn't matter", "-", "yo'q", "yoq", "kerak emas"]


def _past(matn):
    return " " + alifbo.lotin_uz(matn or "").lower().replace("’", "'").replace("‘", "'").replace("ʻ", "'") + " "


def _topish(matn, lugat):
    p = _past(matn)
    for nom, sozlar in lugat.items():
        if any(s in p for s in sozlar):
            return nom
    return None


def tur_aniqla(matn):
    p = _past(matn)
    # «ko'ylak emas, sumka» — «emas» dan keyingi tur ustun
    if " emas" in p:
        keyin = p.split(" emas", 1)[1]
        t = tur_aniqla(keyin)
        if t:
            return t
    topilgan = [(p.find(s), t) for t, sozlar in TUR_SOZLAR.items() for s in sozlar if s in p]
    return min(topilgan)[1] if topilgan else None


# ---------------------------------------------------------------- niyat (amal)
def niyat(matn):
    """Maxsus buyruqlar: bekor, operator, tahrir, boshqa_<maydon>, tasdiq."""
    p = _past(matn)
    if any(s in p for s in ["bekor qil", "bekor qiling", "kerak emas buyurtma", "cancel", "отмен"]):
        return "bekor"
    if any(s in p for s in ["tikuvchi bilan gaplash", "usta bilan gaplash", "hunarmand bilan gaplash",
                            "operator", "odam bilan gaplash", "talk to", "оператор"]):
        return "operator"
    if any(s in p for s in ["oldingi javob", "javobimni o'zgartir", "o'zgartirmoqchiman", "tahrirla", "edit"]):
        return "tahrir"
    m = re.search(r"boshqa (rang|mato|fason|material|naqsh|hajm|shakl|uzunlik|dastak|yoqa)", p)
    if m:
        return "boshqa_" + m.group(1)
    return None


# ---------------------------------------------------------------- holat
def yangi_karta():
    return {"tur": None, "maydonlar": {}, "oxirgi": None, "izoh": ""}


def kerakli(karta):
    """Shu tur uchun hali so'ralmagan maydonlar ro'yxati."""
    t = TURLAR.get(karta.get("tur") or "")
    if not t:
        return []
    return [k for k, _ in t["maydonlar"] if not karta["maydonlar"].get(k)]


def keyingi_savol(karta):
    """(maydon, savol) yoki None — barcha maydon to'lgan bo'lsa."""
    if not karta.get("tur"):
        return ("tur", TUR_TANLASH)
    qolgan = kerakli(karta)
    if not qolgan:
        return None
    savol = dict(TURLAR[karta["tur"]]["maydonlar"])[qolgan[0]]
    return (qolgan[0], savol)


def tur_ornat(karta, tur):
    """Tur almashsa — yangi turga tegishli bo'lmagan maydonlar o'chadi (masalan bo'y, yeng)."""
    if tur == karta.get("tur"):
        return
    eski = karta.get("maydonlar", {})
    kerak = {k for k, _ in TURLAR[tur]["maydonlar"]}
    karta["maydonlar"] = {k: v for k, v in eski.items() if k in kerak}
    # material ⇄ mato bir xil ma'noda
    if "material" in kerak and eski.get("mato") and not karta["maydonlar"].get("material"):
        karta["maydonlar"]["material"] = eski["mato"]
    if "mato" in kerak and eski.get("material") and not karta["maydonlar"].get("mato"):
        karta["maydonlar"]["mato"] = eski["material"]
    karta["tur"] = tur


# ---------------------------------------------------------------- ajratib olish
def tur_almashtirishmi(matn, karta):
    """Tur allaqachon bor bo'lsa — faqat aniq o'zgartirish so'zi bo'lsa almashtiramiz
    («tik yoqa» degan javob aksessuarga, «yengi kalta» degan javob boshqaga o'tib ketmasin)."""
    if not karta.get("tur"):
        return True
    p = _past(matn)
    return any(s in p for s in (" emas", "o'rniga", " kerak", " need", " want", "almashtir", "instead"))


def _offline_ajrat(matn, karta):
    t = tur_aniqla(matn)
    if t and tur_almashtirishmi(matn, karta):
        tur_ornat(karta, t)
    else:
        t = None
    if not karta.get("tur"):
        return
    kerak = {k for k, _ in TURLAR[karta["tur"]]["maydonlar"]}
    topildi = set()
    for maydon, lugat in QIYMAT_SOZLAR.items():
        if maydon in kerak:
            manba = matn
            if maydon == "uzunlik":  # «uzun yengli» — bu yeng, uzunlik emas
                manba = re.sub(r"(uzun|kalta|qisqa)\s+yeng\w*", " ", _past(matn))
            q = _topish(manba, lugat)
            if q:
                karta["maydonlar"][maydon] = q
                topildi.add(maydon)
    # Oxirgi so'ralgan savolga javob — kalit so'z topilmasa ham shu maydonga yoziladi
    oxirgi = karta.get("oxirgi")
    if topildi - {oxirgi}:
        return  # gap boshqa maydonlar haqida — oxirgi savolga javob emas
    if oxirgi in kerak and oxirgi not in topildi and not karta["maydonlar"].get(oxirgi):
        javob = matn.strip()
        if _past(javob).strip() in FARQI_YOQ:
            javob = "farqi yo'q"
        if not (t and len(javob.split()) <= 2 and oxirgi != "tavsif"):
            karta["maydonlar"][oxirgi] = javob[:120]


AI_PROMPT = """You extract a tailoring order from a customer's message for an Uzbek marketplace bot.
Product types and their fields:
{turlar}
Current order card (JSON): {karta}
The bot last asked about field: {oxirgi}
Customer's new message: «{matn}»

Rules:
- If the message names or changes the product type (e.g. "ko'ylak emas, sumka"), set "tur".
- Fill ONLY fields of the current type that the customer actually stated. Never invent values,
  never invent price or deadline. If the message answers the last asked field, fill that field.
- If the customer changes a value ("boshqa rang — qizil"), overwrite it.
- "uzun yengli" is about the sleeve (yeng), not the garment length (uzunlik).
- Write ALL values in short Uzbek Latin (e.g. ikat -> adras, blue -> ko'k, zipper -> fermuar).
Return ONLY JSON: {{"tur": "<type key or null>", "maydonlar": {{"field": "value", ...}}}}"""


def _ai_ajrat(cfg, matn, karta):
    import ai
    turlar = "\n".join("- " + k + ": " + ", ".join(m for m, _ in v["maydonlar"]) for k, v in TURLAR.items())
    prompt = AI_PROMPT.format(turlar=turlar, karta=json.dumps(karta, ensure_ascii=False),
                              oxirgi=karta.get("oxirgi") or "none", matn=matn)
    javob = ai.erkin_soro(cfg, prompt)
    j = json.loads(javob[javob.find("{"): javob.rfind("}") + 1])
    if j.get("tur") in TURLAR and (j["tur"] == karta.get("tur") or tur_almashtirishmi(matn, karta)):
        tur_ornat(karta, j["tur"])
    if karta.get("tur"):
        kerak = {k for k, _ in TURLAR[karta["tur"]]["maydonlar"]}
        for k, v in (j.get("maydonlar") or {}).items():
            if k in kerak and v and str(v).strip().lower() not in ("null", "none", ""):
                karta["maydonlar"][k] = str(v).strip()[:120]


def javobni_qabul(cfg, matn, karta):
    """Mijoz xabarini kartaga qo'shadi.
    Qisqa javoblar (savolga javob) — tez qoida bilan; uzun erkin gap — AI bilan (12 soniyagacha),
    AI ulgurmasa yoki xato bersa — yana qoida bilan. Bot hech qachon to'xtab qolmaydi."""
    import copy
    if not karta.get("izoh"):
        karta["izoh"] = matn[:300]
    oddiy = copy.deepcopy(karta)
    _offline_ajrat(matn, oddiy)
    uzun = len(matn.split()) >= 5 or not karta.get("tur")
    ai_bor = (cfg.get("ai_provider") or "yoq") not in ("yoq", "", "offline")
    if ai_bor and uzun:
        try:
            import threading
            sinov = copy.deepcopy(karta)
            xato = []

            def _ish():
                try:
                    _ai_ajrat(dict(cfg, ai_vaqt=12), matn, sinov)
                except Exception as e:
                    xato.append(e)
            th = threading.Thread(target=_ish, daemon=True)
            th.start()
            th.join(12)  # mijoz 12 soniyadan ortiq kutmaydi
            if th.is_alive() or xato:
                raise TimeoutError("AI ulgurmadi")
            # AI topgan + qoida topgan (qoida faqat AI qoldirgan bo'sh joylarni to'ldiradi)
            for k, v in oddiy.get("maydonlar", {}).items():
                if sinov.get("tur") == oddiy.get("tur"):
                    sinov["maydonlar"].setdefault(k, v)
            karta.clear()
            karta.update(sinov)
            return
        except Exception:
            pass
    karta.clear()
    karta.update(oddiy)


# ---------------------------------------------------------------- ko'rinish
def karta_matni(karta, olcham=None, muddat=None):
    t = TURLAR.get(karta.get("tur") or "", {})
    q = ["• <b>Mahsulot:</b> " + (t.get("nom") or "aniqlanmagan")]
    for k, _ in t.get("maydonlar", []):
        v = karta["maydonlar"].get(k)
        if v:
            q.append("• <b>" + MAYDON_NOMI.get(k, k) + ":</b> " + v)
    if olcham:
        o = [OLCHAM_NOMI[k] + ": " + str(v) for k, v in olcham.items() if v and v != "-" and k in OLCHAM_NOMI]
        if o:
            q.append("• <b>O'lchamlar:</b> " + ", ".join(o))
    if muddat:
        q.append("• <b>Muddat:</b> " + muddat)
    return "\n".join(q)


def tafsilot(karta):
    """Eski tuzilma bilan mos lug'at (hunarmandga ko'rsatish, ro'yxatlar)."""
    d = {"kiyim": TURLAR.get(karta.get("tur") or "", {}).get("nom", "buyurtma"), "tur": karta.get("tur")}
    d.update(karta.get("maydonlar", {}))
    if karta.get("izoh"):
        d["izoh"] = karta["izoh"]
    return d


def tahrir_tugmalari(karta):
    t = TURLAR.get(karta.get("tur") or "", {})
    q, qator = [], []
    for k, _ in t.get("maydonlar", []):
        qator.append((MAYDON_NOMI.get(k, k), "tm_" + k))
        if len(qator) == 3:
            q.append(qator)
            qator = []
    if qator:
        q.append(qator)
    q.append([("🔄 Mahsulot turini almashtirish", "tm_tur")])
    return q


def dizayndan(d):
    """Tanlangan dizayndan karta: tur va ma'lum qiymatlar oldindan to'ladi."""
    karta = yangi_karta()
    tur = tur_aniqla((d.get("kiyim") or "") + " " + (d.get("nom") or "")) or "ko'ylak"
    tur_ornat(karta, tur)
    kerak = {k for k, _ in TURLAR[tur]["maydonlar"]}
    for k in ("mato", "rang", "material"):
        if k in kerak and d.get("mato" if k == "material" else k):
            karta["maydonlar"][k] = d.get("mato" if k == "material" else k)
    if "fason" in kerak:
        karta["maydonlar"]["fason"] = "namuna bo'yicha"
    if tur == "aksessuar":
        karta["maydonlar"]["turi"] = d.get("kiyim") or d.get("nom")
        karta["maydonlar"]["dizayn"] = "namuna bo'yicha"
    karta["izoh"] = "Tayyor dizayn: " + d.get("nom", "") + " (kod: " + d.get("id", "") + ")"
    return karta
