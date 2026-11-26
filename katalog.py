# -*- coding: utf-8 -*-
"""
Chevar AI — kataloglar:
  🧵 Milliy matolar  — xususiyatlari va qaysi kiyimga mosligi; «shu matodan buyurtma»
  📐 O'lchamlar      — ayollar, erkaklar, bolalar o'lcham jadvali + o'lcham bo'yicha maslahat
  🎓 Akademiya       — kashtachilik, zardo'zlik, ko'rpachado'zlik, tikuvchilik video darslari

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

import urllib.parse

from core import (DATA, admin_mi, holat, holat_ol, holat_tozala, saqla, tugmalar, vaqt, yubor)

# =====================  Milliy matolar  =====================

MATOLAR = [
    {"kod": "atlas", "nom": "Atlas (xon atlas)", "tarkib": "100% ipak",
     "xususiyat": "Abrbandi usulida to'qiladi: iplar to'qishdan oldin bo'yaladi, shuning uchun naqsh "
                  "chetlari «yoyilgan» ko'rinadi. Yaltiroq, sirpanchiq, yengil.",
     "mos": "ayollar ko'ylagi, lozim, to'y va bayram libosi, ro'mol",
     "parvarish": "qo'lda, sovuq suvda; burab siqmang, teskari tomonidan dazmollang"},
    {"kod": "adras", "nom": "Adras", "tarkib": "ipak tanda + paxta arqoq",
     "xususiyat": "Atlasdan qalinroq va chidamliroq, yaltirashi xiraroq. Abrband naqshlari bilan. "
                  "Zamonaviy kiyimlarda eng ko'p ishlatiladigan milliy mato.",
     "mos": "ko'ylak, chapan, nimcha, kurtka, yubka, sumka, yostiq jildi",
     "parvarish": "qo'lda yoki yumshoq rejimda 30°C, alohida yuving (rang berishi mumkin)"},
    {"kod": "beqasam", "nom": "Beqasam", "tarkib": "ipak va paxta aralash",
     "xususiyat": "Zich, qalin, ko'pincha yo'l-yo'l (polosali) naqshli. Shakl saqlaydi, uzoq yaraydi.",
     "mos": "erkaklar chaponi va to'ni, kamzul, ko'rpacha jildi",
     "parvarish": "kimyoviy tozalash yoki qo'lda yuvish"},
    {"kod": "shoyi", "nom": "Shoyi", "tarkib": "100% ipak",
     "xususiyat": "Yupqa, mayin, havo o'tkazadi, tanaga yoqimli. Bir xil rangli yoki bosma naqshli.",
     "mos": "ro'mol, bluzka, ko'ylak, kiyim astari",
     "parvarish": "qo'lda, sovuq suvda, ipak uchun vosita bilan"},
    {"kod": "baxmal", "nom": "Baxmal", "tarkib": "ipak yoki paxta asosida tukli mato",
     "xususiyat": "Tukli, og'ir, issiq, nur tushganda tovlanadi. Zardo'zi va kashta uchun ajoyib asos.",
     "mos": "kelin do'ppisi, nimcha, chapan, yoqa, kechki libos",
     "parvarish": "faqat kimyoviy tozalash; dazmolni tegizmay bug' bilan"},
    {"kod": "alacha", "nom": "Alacha", "tarkib": "paxta (ba'zan ipak qo'shilgan)",
     "xususiyat": "Yo'l-yo'l, pishiq, kundalik foydalanishga chidamli an'anaviy mato.",
     "mos": "erkaklar to'ni, yaktak, ko'rpacha, sumka",
     "parvarish": "mashinada 30–40°C"},
    {"kod": "chit", "nom": "Chit", "tarkib": "100% paxta",
     "xususiyat": "Yengil, arzon, bosma gulli. Issiq kunlar uchun qulay.",
     "mos": "kundalik ko'ylak, lozim, ro'mol, bolalar kiyimi",
     "parvarish": "mashinada 40°C"},
    {"kod": "movut", "nom": "Qizil movut / jun mato", "tarkib": "jun",
     "xususiyat": "Qalin, issiq, shakl saqlaydi. Qoraqalpoq an'anaviy kiyimlarida qizil mato ustiga "
                  "kashta tikiladi.",
     "mos": "qoraqalpoq kashtali libosi, chapan, nimcha, palto, belbog'",
     "parvarish": "kimyoviy tozalash"},
]


def matolar_royxati(uid):
    q = [[(m["nom"], "mt_" + m["kod"])] for m in MATOLAR]
    yubor(uid, "🧵 <b>Milliy matolar katalogi</b>\n\nMatoni tanlang — xususiyati va qaysi kiyimga "
               "mosligini ko'rasiz:", kb=tugmalar(q))


def mato_korsat(uid, kod):
    m = next((x for x in MATOLAR if x["kod"] == kod), None)
    if not m:
        return
    yubor(uid, "🧵 <b>" + m["nom"] + "</b>\n\n"
               "<b>Tarkibi:</b> " + m["tarkib"] + "\n"
               "<b>Xususiyati:</b> " + m["xususiyat"] + "\n\n"
               "✂️ <b>Mos kiyimlar:</b> " + m["mos"] + "\n"
               "🧼 <b>Parvarish:</b> " + m["parvarish"],
          kb=tugmalar([[("🤖 Shu matodan buyurtma berish", "mtb_" + kod)],
                       [("⬅️ Boshqa matolar", "kt_mato")]]))


def mato_nomi(kod):
    m = next((x for x in MATOLAR if x["kod"] == kod), None)
    return (m["kod"] if m else kod)


# =====================  O'lchamlar  =====================

# (o'lcham, xalqaro, ko'krak, bel, son) — sm
AYOL = [("42", "XS", 84, 66, 92), ("44", "S", 88, 70, 96), ("46", "M", 92, 74, 100),
        ("48", "L", 96, 78, 104), ("50", "XL", 100, 82, 108), ("52", "XXL", 104, 86, 112),
        ("54", "3XL", 108, 90, 116), ("56", "4XL", 112, 94, 120)]
ERKAK = [("46", "S", 92, 80, 96), ("48", "M", 96, 84, 100), ("50", "L", 100, 88, 104),
         ("52", "XL", 104, 92, 108), ("54", "XXL", 108, 96, 112), ("56", "3XL", 112, 100, 116)]
# (bo'y, ko'krak, bel, son)
BOLA = [(104, 56, 53, 60), (110, 58, 54, 62), (116, 60, 55, 64), (122, 62, 56, 66),
        (128, 64, 57, 68), (134, 66, 58, 71), (140, 70, 60, 74), (146, 72, 61, 77), (152, 76, 63, 80)]

OLCHASH = ("📏 <b>O'zingizni qanday o'lchaysiz</b>\n"
           "• <b>Ko'krak</b> — eng bo'rtgan joyidan, lenta gorizontal\n"
           "• <b>Bel</b> — eng ingichka joyidan\n"
           "• <b>Son</b> — eng keng joyidan\n"
           "• <b>Bo'y</b> — tovondan boshning tepasigacha, poyabzalsiz\n"
           "<i>Lentani tortmang va bo'sh ham qo'ymang.</i>")


def _jadval(nom, qator):
    if nom == "bola":
        return "\n".join("<code>" + str(b).rjust(3) + " sm │ " + str(k).rjust(3) + " │ " + str(be).rjust(3)
                         + " │ " + str(s).rjust(3) + "</code>" for b, k, be, s in qator)
    return "\n".join("<code>" + o.rjust(2) + " " + x.ljust(4) + "│ " + str(k).rjust(3) + " │ "
                     + str(b).rjust(3) + " │ " + str(s).rjust(3) + "</code>" for o, x, k, b, s in qator)


def olchamlar(uid, tur=None):
    if tur is None:
        yubor(uid, "📐 <b>O'lchamlar katalogi</b>\n\nQaysi jadval kerak?",
              kb=tugmalar([[("👩 Ayollar", "oj_ayol"), ("👨 Erkaklar", "oj_erkak"), ("🧒 Bolalar", "oj_bola")],
                           [("📏 O'zimni qanday o'lchayman?", "oj_qanday")]]))
        return
    if tur == "qanday":
        yubor(uid, OLCHASH)
        return
    if tur == "bola":
        yubor(uid, "🧒 <b>Bolalar o'lchami</b> (sm)\n<code>Bo'y    │ Ko'k│ Bel │ Son</code>\n"
              + _jadval("bola", BOLA) + "\n\n<i>Bolalarda o'lcham asosan bo'yga qarab tanlanadi.</i>")
        return
    qator = AYOL if tur == "ayol" else ERKAK
    yubor(uid, ("👩 <b>Ayollar" if tur == "ayol" else "👨 <b>Erkaklar") + " o'lchami</b> (sm)\n"
          "<code>O'lchm │ Ko'k│ Bel │ Son</code>\n" + _jadval(tur, qator)
          + "\n\n<i>Ikki o'lcham oralig'ida bo'lsangiz — kattasini tanlang, usta toraytiradi.</i>",
          kb=tugmalar([[("📏 O'zimni qanday o'lchayman?", "oj_qanday")]]))


# ---------- maslahat (buyurtma paytida)

def _vazndan(jins, vazn):
    chegaralar = ([50, 56, 62, 68, 74, 80, 88] if jins == "ayol" else [62, 70, 78, 86, 95])
    qator = AYOL if jins == "ayol" else ERKAK
    i = sum(1 for c in chegaralar if vazn > c)
    return min(i, len(qator) - 1)


def maslahat_boshla(uid):
    h = holat_ol(uid)
    h["maslahat"] = {}
    holat(uid, "maslahat")
    saqla()
    yubor(uid, "🤖 Yaxshi, o'lchamni birga tanlaymiz.\nKim uchun tikiladi?",
          kb=tugmalar([[("👩 Ayol", "ms_ayol"), ("👨 Erkak", "ms_erkak"), ("🧒 Bola", "ms_bola")]]))


def maslahat_jins(uid, jins):
    h = holat_ol(uid)
    if h.get("bosqich") != "maslahat":
        return
    h["maslahat"] = {"jins": jins}
    saqla()
    yubor(uid, "📏 Bo'yi necha sm? (masalan: 165)")


def maslahat_matn(uid, matn):
    h = holat_ol(uid)
    m = h.setdefault("maslahat", {})
    son = int("".join(c for c in matn if c.isdigit()) or 0)
    if not m.get("jins"):
        yubor(uid, "Kim uchun tikilishini tugma bilan tanlang.")
        return
    if "boy" not in m:
        if not 60 <= son <= 220:
            yubor(uid, "Bo'yni santimetrda yozing, masalan: 165")
            return
        m["boy"] = son
        saqla()
        if m["jins"] == "bola":
            _variantlar(uid)
        else:
            yubor(uid, "⚖️ Vazni taxminan necha kg? (masalan: 60)")
        return
    if not 25 <= son <= 200:
        yubor(uid, "Vaznni kilogrammda yozing, masalan: 60")
        return
    m["vazn"] = son
    saqla()
    _variantlar(uid)


def _variantlar(uid):
    h = holat_ol(uid)
    m = h["maslahat"]
    if m["jins"] == "bola":
        i = min(range(len(BOLA)), key=lambda k: abs(BOLA[k][0] - m["boy"]))
        tanlov = [j for j in (i, i + 1) if j < len(BOLA)]
        tugma = [[(str(BOLA[j][0]) + " (" + ("mos" if j == i else "o'sishga") + ")", "mv_" + str(j))] for j in tanlov]
        izoh = "Bo'yi " + str(m["boy"]) + " sm — eng yaqin o'lcham <b>" + str(BOLA[i][0]) + "</b>."
    else:
        qator = AYOL if m["jins"] == "ayol" else ERKAK
        i = _vazndan(m["jins"], m["vazn"])
        tanlov = [j for j in (i - 1, i, i + 1) if 0 <= j < len(qator)]
        tugma = [[(qator[j][0] + " (" + qator[j][1] + ")" + (" — tavsiya" if j == i else ""), "mv_" + str(j))]
                 for j in tanlov]
        izoh = ("Bo'y " + str(m["boy"]) + " sm, vazn " + str(m["vazn"]) + " kg bo'yicha sizga taxminan <b>"
                + qator[i][0] + " (" + qator[i][1] + ")</b> mos keladi: ko'krak " + str(qator[i][2])
                + ", bel " + str(qator[i][3]) + ", son " + str(qator[i][4]) + " sm.")
    yubor(uid, "🤖 " + izoh + "\n\nVariantlardan birini tanlang — kartaga yozib qo'yaman.\n"
               "<i>Bu taxminiy tavsiya: aniq o'lchamni usta primerkada tekshiradi.</i>",
          kb=tugmalar(tugma + [[("📏 O'zim o'lchab yozaman", "mv_qol")]]))


def variant_tanlandi(uid, indeks):
    """Tanlangan o'lchamni buyurtmaga yozadi. True — o'lcham yozildi."""
    h = holat_ol(uid)
    m = h.get("maslahat") or {}
    if h.get("bosqich") != "maslahat" or "jins" not in m:
        return False
    if indeks == "qol":
        return False
    j = int(indeks)
    o = h.setdefault("olcham", {})
    kerak = h.get("olcham_royxat", [])
    if m["jins"] == "bola":
        b, k, be, s = BOLA[j]
        o["razmer"] = "bolalar " + str(b)
        qiymat = {"boy": m.get("boy", b), "kokrak": k, "bel": be, "son": s}
    else:
        qator = AYOL if m["jins"] == "ayol" else ERKAK
        r, x, k, be, s = qator[j]
        o["razmer"] = r + " (" + x + ")" + (" ayollar" if m["jins"] == "ayol" else " erkaklar")
        qiymat = {"boy": m.get("boy"), "kokrak": k, "bel": be, "son": s}
    for kalit in kerak:
        if qiymat.get(kalit):
            o[kalit] = str(qiymat[kalit]) + " (jadvaldan)" if kalit != "boy" else str(qiymat[kalit])
    saqla()
    yubor(uid, "✅ Yozib qo'ydim: <b>" + o["razmer"] + "</b>")
    return True


# =====================  Hunarmandchilik akademiyasi  =====================

HUNARLAR = ["Kashtachilik", "Zardo'zlik", "Ko'rpachado'zlik", "Tikuvchilik", "Boshqa hunarlar"]
QIDIRUV = {"Kashtachilik": "kashtachilik darsi", "Zardo'zlik": "zardo'zlik darsi",
           "Ko'rpachado'zlik": "ko'rpacha tikish", "Tikuvchilik": "tikuvchilik darsi boshlang'ich",
           "Boshqa hunarlar": "milliy hunarmandchilik darsi"}


def akademiya(uid):
    darslar = DATA.setdefault("darslar", [])
    q = [[(h + " (" + str(sum(1 for d in darslar if d["hunar"] == h)) + ")", "ak_" + str(i))]
         for i, h in enumerate(HUNARLAR)]
    yubor(uid, "🎓 <b>Hunarmandchilik akademiyasi</b>\n\nVideo darslar. Qaysi hunar?", kb=tugmalar(q))


def hunar_darslari(uid, i):
    hunar = HUNARLAR[i]
    darslar = [d for d in DATA.get("darslar", []) if d["hunar"] == hunar]
    if not darslar:
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(QIDIRUV[hunar])
        yubor(uid, "🎓 <b>" + hunar + "</b>\n\nBu bo'limga darslar tez orada joylanadi.\n"
                   "Hozircha YouTube'dagi darslarni ko'rishingiz mumkin:\n" + url)
        return
    yubor(uid, "🎓 <b>" + hunar + "</b> — " + str(len(darslar)) + " ta dars")
    from core import api
    for d in darslar[:15]:
        izoh = "▶️ <b>" + d["nom"] + "</b>" + ("\n" + d["tavsif"] if d.get("tavsif") else "")
        if d.get("video"):
            api("sendVideo", chat_id=uid, video=d["video"], caption=izoh, parse_mode="HTML")
        else:
            yubor(uid, izoh + "\n" + d.get("havola", ""))


def dars_qosh_boshla(uid):
    holat(uid, "dars", dars={})
    saqla()
    yubor(uid, "🎓 <b>Yangi dars</b> — qaysi hunar?",
          kb=tugmalar([[(h, "dq_" + str(i))] for i, h in enumerate(HUNARLAR)]))


def dars_hunar(uid, i):
    h = holat_ol(uid)
    if h.get("bosqich") != "dars":
        return
    h["dars"] = {"hunar": HUNARLAR[i]}
    saqla()
    yubor(uid, "📝 Dars nomi? (masalan: «Zardo'zlik: 1-dars, asboblar»)")


def dars_davom(uid, msg, matn):
    """Admin: nom → tavsif → video (fayl) yoki havola."""
    h = holat_ol(uid)
    d = h.get("dars", {})
    if "hunar" not in d:
        yubor(uid, "Avval hunarni tugma bilan tanlang.")
        return
    if "nom" not in d:
        d["nom"] = matn[:120]
        saqla()
        yubor(uid, "✏️ Qisqa tavsif? (yo'q bo'lsa «-»)")
        return
    if "tavsif" not in d:
        d["tavsif"] = "" if matn.strip() == "-" else matn[:400]
        saqla()
        yubor(uid, "🎬 Endi videoni yuboring yoki havola (YouTube va h.k.) yozing.")
        return
    video = (msg.get("video") or msg.get("document") or {}).get("file_id", "")
    havola = matn if matn.startswith("http") else ""
    if not video and not havola:
        yubor(uid, "Video fayl yuboring yoki http bilan boshlanadigan havola yozing.")
        return
    d.update({"video": video, "havola": havola, "id": len(DATA.setdefault("darslar", [])) + 1,
              "qoshildi": vaqt()})
    DATA["darslar"].append(d)
    holat_tozala(uid)
    saqla()
    yubor(uid, "✅ Dars qo'shildi: <b>" + d["nom"] + "</b> (" + d["hunar"] + ")")


# =====================  Kataloglar menyusi  =====================

def kataloglar(uid):
    q = [[("🧵 Milliy matolar", "kt_mato")], [("📐 O'lchamlar", "kt_olcham")],
         [("🎓 Hunarmandchilik akademiyasi", "kt_akad")]]
    if admin_mi(uid):
        q.append([("➕ Akademiyaga dars qo'shish", "kt_dq")])
    yubor(uid, "📚 <b>Kataloglar</b>", kb=tugmalar(q))
