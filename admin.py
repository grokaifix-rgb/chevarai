# -*- coding: utf-8 -*-
"""
Chevar AI — admin panel: statistika, hunarmandlar, dizayn va mahsulot qo'shish,
do'kon buyurtmalarini boshqarish.

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

from core import (DATA, ADMINLAR, KOMISSIYA, admin_mi, holat, holat_ol,
                  usta_reyting,
                  holat_tozala, profil, pul, rasm_yubor, saqla, tahrirla,
                  tugmalar, vaqt, yubor)
import dokon


# =====================  Panel  =====================

def panel(uid):
    bs = list(DATA["buyurtmalar"].values())
    sotuvlar = list(DATA["sotuvlar"].values())
    ustalar = [p for p in DATA["foydalanuvchilar"].values() if p.get("rol") == "usta"]
    kutayotgan = [u for u, p in DATA["foydalanuvchilar"].items()
                  if p.get("rol") == "usta" and not p.get("tasdiq")]
    yakun = [b for b in bs if b["holat"] == "yakunlandi"]
    sotildi = [s for s in sotuvlar if s["holat"] in ("tolangan", "yolda", "topshirildi")]

    tikish_aylanma = sum(b.get("umumiy_narx", 0) for b in yakun)
    tikish_foyda = sum(b.get("umumiy_narx", 0) - b.get("usta_narx", 0) for b in yakun)
    dokon_aylanma = sum(s.get("umumiy", 0) for s in sotildi)

    yubor(uid,
          "🛠 <b>Admin panel</b>\n\n"
          "👥 Foydalanuvchilar: " + str(len(DATA["foydalanuvchilar"])) + "\n"
          "🪡 Hunarmandlar: " + str(len(ustalar))
          + " (kutayotgan: " + str(len(kutayotgan)) + ")\n\n"
          "<b>🤖 Tikish buyurtmalari</b>\n"
          "   Jami: " + str(len(bs)) + " · yakunlangan: " + str(len(yakun)) + "\n"
          "   Aylanma: " + pul(tikish_aylanma) + "\n"
          "   Foyda: <b>" + pul(tikish_foyda) + "</b>\n\n"
          "<b>🛍 Do'kon</b>\n"
          "   Buyurtmalar: " + str(len(sotuvlar)) + " · sotilgan: " + str(len(sotildi)) + "\n"
          "   Aylanma: <b>" + pul(dokon_aylanma) + "</b>\n"
          "   Mahsulot turlari: " + str(len(DATA["mahsulotlar"])) + "\n"
          "   Dizayn namunalari: " + str(len(DATA["dizaynlar"])) + "\n\n"
          "📊 Komissiya: " + str(int(KOMISSIYA)) + "%",
          kb=tugmalar([
              [("🪡 Hunarmandlar", "a_ustalar"), ("👥 Foydalanuvchilar", "a_foyd")],
              [("🤖 Tikish buyurtmalari", "a_buyurtma"),
               ("🛍 Do'kon buyurtmalari", "a_sotuv")],
              [("👗 Dizayn qo'shish", "a_dizayn_qosh")],
              [("🛒 Mahsulot qo'shish", "a_mahsulot_qosh")],
              [("📋 Dizayn/mahsulotlar ro'yxati", "a_kontent")],
          ]))


def ustalar(uid):
    kutayotgan = [(u, p) for u, p in DATA["foydalanuvchilar"].items()
                  if p.get("rol") == "usta" and not p.get("tasdiq")]
    if not kutayotgan:
        yubor(uid, "✅ Kutayotgan ariza yo'q.")
        return
    for u, p in kutayotgan[:10]:
        yubor(uid, "🪡 " + (p.get("ism") or "-") + " · " + (p.get("shahar") or "-")
              + "\n" + (p.get("ixtisos") or "-") + " · " + str(p.get("tajriba", "")) + " yil\n"
              + (p.get("tel") or "-") + "\n<code>" + u + "</code>",
              kb=tugmalar([[("✅ Tasdiqlash", "utasdiq_" + u),
                            ("❌ Rad etish", "urad_" + u)]]))


def usta_kartasi(u, p):
    """Hunarmandning to'liq profili — admin uchun, anonimsiz."""
    ort, soni, yakun = usta_reyting(u)
    ishlar = [b for b in DATA["buyurtmalar"].values() if str(b.get("usta")) == str(u)]
    faol = sum(1 for b in ishlar if b["holat"] in ("tasdiqlangan", "tikilmoqda", "tayyor"))
    daromad = sum(b.get("usta_narx", 0) for b in ishlar if b["holat"] == "yakunlandi")
    takliflar = sum(1 for b in DATA["buyurtmalar"].values() if str(u) in b.get("takliflar", {}))
    if p.get("bloklangan"):
        holati = "🚫 bloklangan"
    elif not p.get("tasdiq"):
        holati = "⏳ ariza ko'rib chiqilmoqda"
    elif p.get("pauza"):
        holati = "⏸ dam olishda"
    else:
        holati = "✅ faol"
    ism = (p.get("ism") or "-")
    return ("🪡 <b><a href=\"tg://user?id=" + str(u) + "\">" + ism + "</a></b>\n"
            + ("✈️ @" + p["username"] + "\n" if p.get("username") else "")
            + "📞 " + (p.get("tel") or "-") + "\n"
            "📍 " + (p.get("shahar") or "-") + "\n"
            "🧵 " + (p.get("ixtisos") or "-") + "\n"
            "⏳ Tajriba: " + (p.get("tajriba") or "-") + " yil\n"
            "📌 Holat: " + holati + "\n"
            + ("⭐️ %.1f (%d baho)" % (ort, soni) if soni else "⭐️ baho yo'q") + "\n"
            "📤 Takliflar: " + str(takliflar) + " · 🔧 Faol: " + str(faol)
            + " · ✅ Bajarilgan: " + str(yakun) + "\n"
            "💰 Ishlab topgan: " + pul(daromad) + "\n"
            "🖼 Portfolio: " + str(len(p.get("portfolio", []))) + " ta rasm\n"
            "📅 Qo'shilgan: " + (p.get("qoshildi") or "-") + "\n"
            "🆔 <code>" + str(u) + "</code>")


def hunarmandlar(uid):
    royxat = [(u, p) for u, p in DATA["foydalanuvchilar"].items() if p.get("rol") == "usta"]
    if not royxat:
        yubor(uid, "🪡 Hali ro'yxatdan o'tgan hunarmand yo'q.")
        return
    kutayotgan = [x for x in royxat if not x[1].get("tasdiq")]
    yubor(uid, "🪡 <b>Hunarmandlar: " + str(len(royxat)) + " ta</b>"
          + (" (arizasi kutilmoqda: " + str(len(kutayotgan)) + ")" if kutayotgan else "")
          + "\n<i>Ismni bossangiz — Telegramdagi profili ochiladi.</i>")
    # Avval arizalar, keyin faollar (eng ko'p ish bajargan birinchi)
    royxat.sort(key=lambda x: (bool(x[1].get("tasdiq")), -usta_reyting(x[0])[2]))
    for u, p in royxat[:30]:
        qatorlar = []
        if not p.get("tasdiq"):
            qatorlar.append([("✅ Tasdiqlash", "utasdiq_" + u), ("❌ Rad etish", "urad_" + u)])
        if p.get("portfolio"):
            qatorlar.append([("🖼 Portfolio", "pf_" + u)])
        qatorlar.append([("✅ Blokdan chiqarish", "ublok_" + u) if p.get("bloklangan")
                         else ("🚫 Bloklash", "ublok_" + u)])
        yubor(uid, usta_kartasi(u, p), kb=tugmalar(qatorlar))


# =====================  Foydalanuvchilar (mijozlar)  =====================

TIL_BELGI = {"uz": "🇺🇿", "en": "🇬🇧", "kaa": "🏳️"}


def mijoz_kartasi(u, p):
    """Mijozning to'liq profili — admin uchun."""
    tikish = [b for b in DATA["buyurtmalar"].values() if str(b.get("mijoz")) == str(u)]
    xarid = [x for x in DATA["sotuvlar"].values() if str(x.get("mijoz")) == str(u)]
    sarf = (sum(b.get("umumiy_narx", 0) for b in tikish if b.get("holat") == "yakunlandi")
            + sum(x.get("umumiy", 0) for x in xarid if x.get("holat") in ("tolangan", "yolda", "topshirildi")))
    faol = sum(1 for b in tikish if b.get("holat") not in ("yakunlandi", "bekor"))
    tel = p.get("tel") or next((b.get("mijoz_tel") for b in reversed(tikish) if b.get("mijoz_tel")), "") \
        or next((x.get("tel") for x in reversed(xarid) if x.get("tel")), "")
    manzil = p.get("manzil") or next((x.get("manzil") for x in reversed(xarid) if x.get("manzil")), "")
    savat = sum(int(x.get("soni", 0)) for x in DATA["savatlar"].get(str(u), []))
    rol = {"usta": "🪡 hunarmand", "mijoz": "👤 mijoz"}.get(p.get("rol"), p.get("rol") or "-")
    if admin_mi(u):
        rol = "🛠 admin"
    return ("👤 <b><a href=\"tg://user?id=" + str(u) + "\">" + (p.get("ism") or "Ismsiz") + "</a></b>\n"
            + ("✈️ @" + p["username"] + "\n" if p.get("username") else "")
            + "📞 " + (tel or "—") + "\n"
            + ("📍 " + manzil + "\n" if manzil else "")
            + "🌐 Til: " + TIL_BELGI.get(p.get("til") or "uz", "") + " " + (p.get("til") or "uz") + "\n"
            "🏷 Rol: " + rol + ("  ·  🚫 bloklangan" if p.get("bloklangan") else "") + "\n"
            "📅 Qo'shilgan: " + (p.get("qoshildi") or "—") + "\n"
            "🕒 Oxirgi faollik: " + (p.get("oxirgi") or "—") + "\n"
            "🤖 Tikish buyurtmalari: " + str(len(tikish)) + " (faol: " + str(faol) + ")\n"
            "🛍 Do'kon xaridlari: " + str(len(xarid)) + "\n"
            "🛒 Savatda: " + str(savat) + " ta\n"
            "💰 Jami to'lagan: " + pul(sarf) + "\n"
            "🆔 <code>" + str(u) + "</code>")


def _mijoz_tugmalari(u, p):
    q = []
    if not admin_mi(u):
        q.append([("✅ Blokdan chiqarish", "fblok_" + u) if p.get("bloklangan")
                  else ("🚫 Bloklash", "fblok_" + u)])
    return tugmalar(q) if q else None


def foydalanuvchilar(uid, sahifa=0):
    royxat = [(u, p) for u, p in DATA["foydalanuvchilar"].items() if p.get("rol") != "usta"]
    if not royxat:
        yubor(uid, "👥 Hali foydalanuvchi yo'q.")
        return
    royxat.sort(key=lambda x: x[1].get("oxirgi") or x[1].get("qoshildi") or "", reverse=True)
    jami = len(royxat)
    tillar = {}
    for _, p in royxat:
        tillar[p.get("til") or "uz"] = tillar.get(p.get("til") or "uz", 0) + 1
    boshi = sahifa * 10
    qism = royxat[boshi:boshi + 10]
    q = ["👥 <b>Foydalanuvchilar: " + str(jami) + " ta</b>  ("
         + ", ".join(TIL_BELGI.get(k, k) + " " + str(v) for k, v in tillar.items()) + ")",
         "<i>Oxirgi faollik bo'yicha. Batafsil ko'rish uchun ismni bosing.\n"
         "Qidirish: /topish ism, @username, telefon yoki ID</i>", ""]
    qatorlar = []
    for i, (u, p) in enumerate(qism, boshi + 1):
        nb = sum(1 for b in DATA["buyurtmalar"].values() if str(b.get("mijoz")) == u) \
            + sum(1 for x in DATA["sotuvlar"].values() if str(x.get("mijoz")) == u)
        q.append(str(i) + ". " + (p.get("ism") or "Ismsiz")
                 + (" (@" + p["username"] + ")" if p.get("username") else "")
                 + " " + TIL_BELGI.get(p.get("til") or "uz", "")
                 + (" · 📦 " + str(nb) if nb else "") + (" · 🚫" if p.get("bloklangan") else ""))
        qatorlar.append([(str(i) + ". " + (p.get("ism") or "Ismsiz")[:28], "fk_" + u)])
    nav = []
    if sahifa > 0:
        nav.append(("⬅️ Oldingi", "fsah_" + str(sahifa - 1)))
    if boshi + 10 < jami:
        nav.append(("Keyingi ➡️", "fsah_" + str(sahifa + 1)))
    if nav:
        qatorlar.append(nav)
    yubor(uid, "\n".join(q), kb=tugmalar(qatorlar))


def topish(uid, soz):
    soz = soz.strip().lstrip("@").lower()
    if not soz:
        yubor(uid, "Qidirish: /topish ism, @username, telefon yoki ID")
        return
    topildi = []
    for u, p in DATA["foydalanuvchilar"].items():
        joylar = [u, p.get("ism", ""), p.get("username", ""), p.get("tel", "")]
        if any(soz in str(x).lower().replace(" ", "") for x in joylar if x):
            topildi.append((u, p))
    if not topildi:
        yubor(uid, "🔍 «" + soz + "» bo'yicha hech kim topilmadi.")
        return
    yubor(uid, "🔍 Topildi: " + str(len(topildi)) + " ta")
    for u, p in topildi[:10]:
        if p.get("rol") == "usta":
            yubor(uid, usta_kartasi(u, p))
        else:
            yubor(uid, mijoz_kartasi(u, p), kb=_mijoz_tugmalari(u, p))


def buyurtmalar(uid):
    faol = [b for b in DATA["buyurtmalar"].values()
            if b["holat"] not in ("yakunlandi", "bekor")]
    if not faol:
        yubor(uid, "📦 Faol tikish buyurtmasi yo'q.")
        return
    import bot
    q = ["🤖 <b>Faol tikish buyurtmalari</b>\n"]
    for b in sorted(faol, key=lambda x: int(x["raqam"]), reverse=True)[:20]:
        q.append("#" + b["raqam"] + " · " + bot.HOLAT_NOMI.get(b["holat"], b["holat"])
                 + (" · " + pul(b["umumiy_narx"]) if b.get("umumiy_narx") else ""))
    yubor(uid, "\n".join(q))


def sotuvlar(uid):
    faol = [s for s in DATA["sotuvlar"].values()
            if s["holat"] not in ("topshirildi", "bekor")]
    if not faol:
        yubor(uid, "🛍 Faol do'kon buyurtmasi yo'q.")
        return
    for s in sorted(faol, key=lambda x: int(x["raqam"]), reverse=True)[:10]:
        qatorlar = []
        if s["holat"] == "tekshiruvda":
            qatorlar.append([("✅ To'lovni tasdiqlash", "stol_" + s["raqam"])])
        if s["holat"] == "tolangan":
            qatorlar.append([("🚚 Yo'lga chiqdi", "syol_" + s["raqam"])])
        if s["holat"] == "yolda":
            qatorlar.append([("✅ Topshirildi", "stop_" + s["raqam"])])
        qatorlar.append([("❌ Bekor qilish", "sbekor_" + s["raqam"])])
        yubor(uid, dokon.sotuv_matni(s, ichki=True)
              + "\n\n📌 Holat: " + s["holat"], kb=tugmalar(qatorlar))


def kontent(uid):
    q = ["📋 <b>Dizayn namunalari</b>"]
    if DATA["dizaynlar"]:
        for d in DATA["dizaynlar"].values():
            q.append(("✅" if d.get("faol", True) else "🚫") + " " + d["id"] + " — "
                     + d.get("nom", "") + (" · " + pul(d["narx"]) if d.get("narx") else ""))
    else:
        q.append("   (yo'q)")
    q.append("\n🛒 <b>Mahsulotlar</b>")
    if DATA["mahsulotlar"]:
        for m in DATA["mahsulotlar"].values():
            zax = ", ".join(o + ":" + str(s) for o, s in (m.get("zaxira") or {}).items())
            q.append(("✅" if m.get("faol", True) else "🚫") + " " + m["id"] + " — "
                     + m.get("nom", "") + " · " + pul(m.get("narx", 0)) + " · " + zax)
    else:
        q.append("   (yo'q)")
    q.append("\n<i>O'chirish: /ochir dizayn_kodi (masalan /ochir D3 yoki /ochir M5)</i>")
    yubor(uid, "\n".join(q))


def ochir(uid, kod):
    kod = kod.strip().upper()
    if kod in DATA["dizaynlar"]:
        DATA["dizaynlar"][kod]["faol"] = not DATA["dizaynlar"][kod].get("faol", True)
        saqla()
        yubor(uid, ("✅ Yoqildi: " if DATA["dizaynlar"][kod]["faol"] else "🚫 Yashirildi: ")
              + kod)
    elif kod in DATA["mahsulotlar"]:
        DATA["mahsulotlar"][kod]["faol"] = not DATA["mahsulotlar"][kod].get("faol", True)
        saqla()
        yubor(uid, ("✅ Yoqildi: " if DATA["mahsulotlar"][kod]["faol"] else "🚫 Yashirildi: ")
              + kod)
    else:
        yubor(uid, "Bunday kod topilmadi: " + kod)


# =====================  Dizayn qo'shish  =====================

DIZAYN_SAVOL = [
    ("nom", "👗 Dizayn nomi? (masalan: «Adras milliy ko'ylak — Marg'ilon»)"),
    ("tavsif", "📝 Qisqacha tavsif? (yo'q bo'lsa «-»)"),
    ("kategoriya", "📂 Bo'lim? (masalan: Ko'ylaklar / Nimchalar / Kurtka va chapanlar / "
                   "Sumkalar / Bosh kiyimlar)"),
    ("mato", "🧵 Qanday matodan? (masalan: adras)"),
    ("rang", "🎨 Rangi? (yo'q bo'lsa «-»)"),
    ("narx", "💵 Taxminiy narx (faqat son, bilmasangiz 0):"),
]

MAHSULOT_SAVOL = [
    ("nom", "🛒 Mahsulot nomi?"),
    ("tavsif", "📝 Qisqacha tavsif? (yo'q bo'lsa «-»)"),
    ("kategoriya", "📂 Kategoriya? (masalan: Ayollar / Erkaklar / Bolalar / Aksessuar)"),
    ("narx", "💵 Narxi (faqat son):"),
    ("zaxira", "📏 O'lchamlar va soni?\n<i>Masalan: S:2, M:5, L:3, XL:1</i>"),
]


def qoshish_boshla(uid, tur):
    holat(uid, "qosh", tur=tur, indeks=0, yangi={})
    saqla()
    savollar = DIZAYN_SAVOL if tur == "dizayn" else MAHSULOT_SAVOL
    yubor(uid, ("👗 <b>Yangi dizayn qo'shish</b>" if tur == "dizayn"
                else "🛒 <b>Yangi mahsulot qo'shish</b>")
          + "\n<i>Bekor qilish: /bekor</i>\n\n" + savollar[0][1])


def qoshish_davom(uid, matn):
    h = holat_ol(uid)
    tur = h.get("tur", "dizayn")
    savollar = DIZAYN_SAVOL if tur == "dizayn" else MAHSULOT_SAVOL
    i = h.get("indeks", 0)
    kalit = savollar[i][0]

    qiymat = matn.strip()
    if kalit == "narx":
        son = "".join(c for c in qiymat if c.isdigit())
        if not son and tur == "mahsulot":
            yubor(uid, "❗️ Narxni raqamda yozing.")
            return
        qiymat = int(son or 0)
    elif kalit == "zaxira":
        zaxira = {}
        for bolak in qiymat.replace(";", ",").split(","):
            if ":" in bolak:
                o, s = bolak.split(":", 1)
                son = "".join(c for c in s if c.isdigit())
                if o.strip() and son:
                    zaxira[o.strip().upper()] = int(son)
        if not zaxira:
            yubor(uid, "❗️ Formatni to'g'ri yozing. Masalan: S:2, M:5, L:3")
            return
        qiymat = zaxira
    elif qiymat == "-":
        qiymat = ""

    h.setdefault("yangi", {})[kalit] = qiymat
    i += 1
    if i < len(savollar):
        h["indeks"] = i
        saqla()
        yubor(uid, savollar[i][1])
        return

    holat(uid, "qosh_rasm")
    saqla()
    yubor(uid, "📸 Endi mahsulot/dizayn <b>rasmini</b> yuboring.\n"
               "<i>Rasm bo'lmasa /otkaz yozing.</i>")


def rasm_qabul(uid, file_id):
    h = holat_ol(uid)
    tur = h.get("tur", "dizayn")
    yangi = h.get("yangi", {})
    yangi["rasm"] = file_id or ""
    yangi["faol"] = True
    yangi["qoshildi"] = vaqt()

    if tur == "dizayn":
        kod = "D" + str(DATA["keyingi_dizayn"])
        DATA["keyingi_dizayn"] += 1
        yangi["id"] = kod
        DATA["dizaynlar"][kod] = yangi
        xabar = "✅ Dizayn qo'shildi: <b>" + kod + " — " + yangi.get("nom", "") + "</b>"
    else:
        kod = "M" + str(DATA["keyingi_mahsulot"])
        DATA["keyingi_mahsulot"] += 1
        yangi["id"] = kod
        DATA["mahsulotlar"][kod] = yangi
        xabar = "✅ Mahsulot qo'shildi: <b>" + kod + " — " + yangi.get("nom", "") + "</b>"

    holat_tozala(uid)
    saqla()
    yubor(uid, xabar + "\n\nEndi u mijozlarga ko'rinadi.")


# =====================  Tugmalarni qayta ishlash  =====================

def tugma(uid, data, message_id):
    """Admin tugmalari. True qaytarsa — tugma shu yerda ishlangan."""
    if not admin_mi(uid):
        return False

    if data == "a_foyd":
        foydalanuvchilar(uid)
    elif data == "a_ustalar":
        hunarmandlar(uid)
    elif data == "a_buyurtma":
        buyurtmalar(uid)
    elif data == "a_sotuv":
        sotuvlar(uid)
    elif data == "a_kontent":
        kontent(uid)
    elif data == "a_dizayn_qosh":
        qoshish_boshla(uid, "dizayn")
    elif data == "a_mahsulot_qosh":
        qoshish_boshla(uid, "mahsulot")

    elif data.startswith("utasdiq_"):
        u = data[8:]
        p = profil(u)
        p["tasdiq"] = True
        p["rol"] = "usta"
        saqla()
        tahrirla(uid, message_id, "✅ Tasdiqlandi: " + (p.get("ism") or u))
        import bot
        yubor(int(u), "🎉 <b>Tabriklaymiz!</b> Siz hunarmand sifatida tasdiqlandingiz.\n\n"
                      "Endi yangi buyurtmalar sizga avtomatik keladi.",
              menyu=bot.USTA_MENYU)

    elif data.startswith("fsah_"):
        foydalanuvchilar(uid, int(data[5:]))
    elif data.startswith("fk_"):
        u = data[3:]
        p = DATA["foydalanuvchilar"].get(u)
        if p:
            yubor(uid, mijoz_kartasi(u, p), kb=_mijoz_tugmalari(u, p))
    elif data.startswith("fblok_"):
        u = data[6:]
        if not admin_mi(u):
            p = profil(u)
            p["bloklangan"] = not p.get("bloklangan")
            saqla()
            tahrirla(uid, message_id, mijoz_kartasi(u, p), kb=_mijoz_tugmalari(u, p))

    elif data.startswith("ublok_"):
        u = data[6:]
        p = profil(u)
        p["bloklangan"] = not p.get("bloklangan")
        saqla()
        tahrirla(uid, message_id, usta_kartasi(u, p))
        yubor(uid, ("🚫 Bloklandi: " if p["bloklangan"] else "✅ Blokdan chiqarildi: ")
              + (p.get("ism") or u))

    elif data.startswith("urad_"):
        u = data[5:]
        p = profil(u)
        p["rol"] = "mijoz"
        p["tasdiq"] = False
        saqla()
        tahrirla(uid, message_id, "❌ Rad etildi.")
        yubor(int(u), "Afsuski, arizangiz tasdiqlanmadi. Batafsil ma'lumot uchun "
                      "biz bilan bog'laning.")

    elif data.startswith(("stol_", "syol_", "stop_", "sbekor_")):
        amal, raqam = data.split("_", 1)
        yangi = {"stol": "tolangan", "syol": "yolda", "stop": "topshirildi",
                 "sbekor": "bekor"}[amal]
        nomi = {"tolangan": "✅ To'lov tasdiqlandi", "yolda": "🚚 Yo'lga chiqdi",
                "topshirildi": "✅ Topshirildi", "bekor": "❌ Bekor qilindi"}[yangi]
        if dokon.sotuv_holat_ozgartir(raqam, yangi):
            tahrirla(uid, message_id, nomi + " (#" + raqam + ")")
        else:
            tahrirla(uid, message_id, "ℹ️ #" + raqam + " — bu amal allaqachon bajarilgan "
                                      "yoki hozirgi holatda mumkin emas.")

    elif data.startswith("tolrad_"):
        _, raqam, tur = data.split("_", 2)
        b = DATA["buyurtmalar"].get(raqam)
        if b:
            b["tolov"]["holat"] = "rad"
            saqla()
            yubor(b["mijoz"], "❗️ To'lov cheki tasdiqlanmadi. Iltimos, qayta "
                              "tekshirib yuboring yoki biz bilan bog'laning.")
        tahrirla(uid, message_id, "❌ To'lov rad etildi (#" + raqam + ")")
    elif data.startswith("tol_"):
        _, raqam, tur = data.split("_", 2)
        import bot
        if bot.tolov_tasdiq(raqam, tur):
            tahrirla(uid, message_id, "✅ To'lov tasdiqlandi (#" + raqam + ")")
        else:
            tahrirla(uid, message_id, "ℹ️ #" + raqam + " to'lovi allaqachon ko'rib "
                                      "chiqilgan (boshqa admin tasdiqlagan bo'lishi mumkin).")
    else:
        return False
    return True
