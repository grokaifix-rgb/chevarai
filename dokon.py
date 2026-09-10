# -*- coding: utf-8 -*-
"""
Chevar AI — Dizaynlar bo'limi va Do'kon (tayyor mahsulotlar) + yetkazib berish.

Dizaynlar: hunarmandlar tayyorlagan namunalar. Mijoz yoqqanini tanlaydi va
o'z o'lchamiga tiktiradi.
Do'kon: tayyor, o'lchami aniq mahsulotlar — savatga solib sotib olinadi.

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

import time

from core import (DATA, ADMINLAR, KARTA, KARTA_EGASI, YETKAZISH_NARX,
                  BEPUL_CHEGARA, adminlarga, holat, holat_ol, holat_tozala,
                  profil, pul, rasm_yubor, saqla, tugmalar, vaqt, yubor)

OLCHAMLAR = ["S", "M", "L", "XL", "XXL", "3XL"]


# =====================  DIZAYNLAR BO'LIMI  =====================

def faol_dizaynlar():
    return [d for d in DATA["dizaynlar"].values() if d.get("faol", True)]


def dizaynlar_royxati(uid, sahifa=0):
    royxat = faol_dizaynlar()
    if not royxat:
        yubor(uid, "👗 <b>Dizaynlar bo'limi</b>\n\n"
                   "Hozircha namunalar joylanmagan.\n"
                   "Tez orada hunarmandlarimiz ishlarini shu yerga qo'shamiz.\n\n"
                   "Shu orada «🤖 AI bilan buyurtma» orqali o'z fikringizni "
                   "aytib buyurtma bersangiz bo'ladi.")
        return

    royxat.sort(key=lambda d: d.get("id", ""))
    boshi = sahifa * 5
    qism = royxat[boshi:boshi + 5]
    if not qism:
        yubor(uid, "Boshqa namuna yo'q.")
        return

    yubor(uid, "👗 <b>Tayyor dizaynlar</b> — yoqqanini tanlang, "
               "o'z o'lchamingizga tikib beramiz.")
    for d in qism:
        matn = ("<b>" + d.get("nom", "Dizayn") + "</b>\n"
                + (d.get("tavsif", "") or "") + "\n"
                + ("🧵 Mato: " + d["mato"] + "\n" if d.get("mato") else "")
                + ("💵 Taxminiy narx: " + pul(d["narx"]) + "\n" if d.get("narx") else ""))
        kb = tugmalar([[("🧵 Shu dizaynda buyurtma berish", "dz_" + d["id"])]])
        if d.get("rasm"):
            rasm_yubor(uid, d["rasm"], matn, kb)
        else:
            yubor(uid, matn, kb=kb)

    if len(royxat) > boshi + 5:
        yubor(uid, "Yana namunalar bor:",
              kb=tugmalar([[("⬇️ Ko'proq ko'rsatish", "dzsah_" + str(sahifa + 1))]]))


def dizayn_tanlandi(uid, dizayn_id):
    d = DATA["dizaynlar"].get(dizayn_id)
    if not d:
        yubor(uid, "Bu dizayn topilmadi.")
        return
    tafsilot = {
        "kiyim": d.get("kiyim") or d.get("nom", ""),
        "mato": d.get("mato", ""),
        "rang": d.get("rang", ""),
        "fason": d.get("fason", "namuna bo'yicha"),
        "izoh": "Tayyor dizayn: " + d.get("nom", "") + " (kod: " + dizayn_id + ")",
    }
    holat(uid, "olcham", buyurtma=tafsilot, olcham={}, olcham_indeks=0,
          dizayn=dizayn_id, dizayn_rasm=d.get("rasm", ""))
    saqla()
    yubor(uid, "✅ <b>" + d.get("nom", "Dizayn") + "</b> tanlandi.\n\n"
               "📏 Endi o'lchamlaringizni olamiz — shunda aynan sizga tikiladi.")
    import bot
    bot.olcham_sora(uid, 0)


# =====================  DO'KON: mahsulotlar  =====================

def faol_mahsulotlar():
    return [m for m in DATA["mahsulotlar"].values()
            if m.get("faol", True) and jami_zaxira(m) > 0]


def jami_zaxira(m):
    return sum(int(v) for v in (m.get("zaxira") or {}).values())


def dokon_kategoriyalar(uid):
    royxat = faol_mahsulotlar()
    if not royxat:
        yubor(uid, "🛍 <b>Do'kon</b>\n\n"
                   "Hozircha sotuvda mahsulot yo'q.\n"
                   "Tez orada tayyor kiyimlar joylanadi.")
        return
    katlar = sorted({(m.get("kategoriya") or "Boshqa") for m in royxat})
    qatorlar = [[(k + " (" + str(len([m for m in royxat
                                      if (m.get("kategoriya") or "Boshqa") == k])) + ")",
                  "kat_" + k)] for k in katlar]
    qatorlar.append([("🛍 Hammasi", "kat_*")])
    yubor(uid, "🛍 <b>Do'kon</b> — tayyor mahsulotlar\n\n"
               "O'lchami aniq, darhol yuboriladi. Bo'limni tanlang:",
          kb=tugmalar(qatorlar))


def mahsulotlar_royxati(uid, kategoriya="*"):
    royxat = faol_mahsulotlar()
    if kategoriya != "*":
        royxat = [m for m in royxat if (m.get("kategoriya") or "Boshqa") == kategoriya]
    if not royxat:
        yubor(uid, "Bu bo'limda hozircha mahsulot yo'q.")
        return
    for m in royxat[:10]:
        olch = ", ".join(o for o, s in (m.get("zaxira") or {}).items() if int(s) > 0)
        matn = ("<b>" + m.get("nom", "") + "</b>\n"
                + (m.get("tavsif", "") or "") + "\n\n"
                + "💵 Narx: <b>" + pul(m.get("narx", 0)) + "</b>\n"
                + "📏 Mavjud o'lchamlar: " + (olch or "-"))
        kb = tugmalar([[("🛒 Savatga qo'shish", "mh_" + m["id"])]])
        if m.get("rasm"):
            rasm_yubor(uid, m["rasm"], matn, kb)
        else:
            yubor(uid, matn, kb=kb)


def olcham_tanlash(uid, mahsulot_id):
    m = DATA["mahsulotlar"].get(mahsulot_id)
    if not m:
        yubor(uid, "Mahsulot topilmadi.")
        return
    mavjud = [(o, s) for o, s in (m.get("zaxira") or {}).items() if int(s) > 0]
    if not mavjud:
        yubor(uid, "Afsuski, bu mahsulot tugagan.")
        return
    qatorlar = []
    qator = []
    for o, s in mavjud:
        qator.append((o + " (" + str(s) + " ta)", "olch_" + mahsulot_id + "_" + o))
        if len(qator) == 3:
            qatorlar.append(qator)
            qator = []
    if qator:
        qatorlar.append(qator)
    yubor(uid, "📏 <b>" + m["nom"] + "</b> — o'lchamni tanlang:", kb=tugmalar(qatorlar))


def savatga_qosh(uid, mahsulot_id, olcham):
    m = DATA["mahsulotlar"].get(mahsulot_id)
    if not m or int((m.get("zaxira") or {}).get(olcham, 0)) <= 0:
        yubor(uid, "Afsuski, bu o'lcham tugagan.")
        return
    savat = DATA["savatlar"].setdefault(str(uid), [])
    for x in savat:
        if x["mahsulot"] == mahsulot_id and x["olcham"] == olcham:
            if x["soni"] + 1 > int(m["zaxira"][olcham]):
                yubor(uid, "Bu o'lchamdan bor-yo'g'i " + str(m["zaxira"][olcham]) + " ta qolgan.")
                return
            x["soni"] += 1
            break
    else:
        savat.append({"mahsulot": mahsulot_id, "olcham": olcham, "soni": 1})
    saqla()
    yubor(uid, "🛒 <b>" + m["nom"] + "</b> (" + olcham + ") savatga qo'shildi.",
          kb=tugmalar([[("🛒 Savatni ko'rish", "savat")],
                       [("🛍 Xaridni davom ettirish", "dokon")]]))


# =====================  SAVAT  =====================

def savat_jami(uid):
    jami = 0
    for x in DATA["savatlar"].get(str(uid), []):
        m = DATA["mahsulotlar"].get(x["mahsulot"])
        if m:
            jami += int(m.get("narx", 0)) * int(x["soni"])
    return jami


def savat_korsat(uid):
    savat = DATA["savatlar"].get(str(uid), [])
    if not savat:
        yubor(uid, "🛒 Savatingiz bo'sh.\n\n«🛍 Do'kon» bo'limidan mahsulot tanlang.")
        return
    q = ["🛒 <b>Savatingiz</b>\n"]
    qatorlar = []
    for i, x in enumerate(savat):
        m = DATA["mahsulotlar"].get(x["mahsulot"])
        if not m:
            continue
        summa = int(m.get("narx", 0)) * int(x["soni"])
        q.append(str(i + 1) + ". " + m["nom"] + " · " + x["olcham"] + " · "
                 + str(x["soni"]) + " ta = <b>" + pul(summa) + "</b>")
        qatorlar.append([("➖", "kam_" + str(i)), (m["nom"][:18], "hech"),
                         ("➕", "kop_" + str(i)), ("🗑", "och_" + str(i))])

    jami = savat_jami(uid)
    yetkazish = 0 if jami >= BEPUL_CHEGARA else YETKAZISH_NARX
    q.append("\n💵 Mahsulotlar: <b>" + pul(jami) + "</b>")
    q.append("🚚 Yetkazib berish: <b>"
             + ("bepul 🎉" if yetkazish == 0 else pul(yetkazish)) + "</b>")
    q.append("🧾 Jami: <b>" + pul(jami + yetkazish) + "</b>")
    if yetkazish and jami < BEPUL_CHEGARA:
        q.append("\n<i>" + pul(BEPUL_CHEGARA) + " dan yuqori xaridda yetkazish bepul.</i>")

    qatorlar.append([("✅ Rasmiylashtirish", "rasmiy")])
    qatorlar.append([("🗑 Savatni bo'shatish", "savat_toza")])
    yubor(uid, "\n".join(q), kb=tugmalar(qatorlar))


def savat_ozgartir(uid, indeks, amal):
    savat = DATA["savatlar"].get(str(uid), [])
    if indeks >= len(savat):
        return
    x = savat[indeks]
    m = DATA["mahsulotlar"].get(x["mahsulot"], {})
    if amal == "kop":
        bor = int((m.get("zaxira") or {}).get(x["olcham"], 0))
        if x["soni"] + 1 > bor:
            yubor(uid, "Bu o'lchamdan " + str(bor) + " ta qolgan.")
            return
        x["soni"] += 1
    elif amal == "kam":
        x["soni"] -= 1
        if x["soni"] <= 0:
            savat.pop(indeks)
    else:
        savat.pop(indeks)
    saqla()
    savat_korsat(uid)


# =====================  RASMIYLASHTIRISH + YETKAZIB BERISH  =====================

def rasmiylashtirish_boshla(uid):
    if not DATA["savatlar"].get(str(uid)):
        yubor(uid, "🛒 Savatingiz bo'sh.")
        return
    holat(uid, "sotuv_usul")
    saqla()
    yubor(uid, "🚚 <b>Qanday olasiz?</b>",
          kb=tugmalar([
              [("🏠 Yetkazib berish", "us_yetkazish")],
              [("🏪 O'zim olib ketaman", "us_olib")],
          ]))


def usul_tanlandi(uid, usul):
    h = holat(uid, "sotuv_manzil" if usul == "yetkazish" else "sotuv_tel")
    h["usul"] = usul
    saqla()
    if usul == "yetkazish":
        yubor(uid, "📍 Yetkazib beriladigan manzilni to'liq yozing.\n\n"
                   "<i>Masalan: Xorazm viloyati, Urganch shahri, Al-Xorazmiy ko'chasi 12-uy</i>")
    else:
        yubor(uid, "📞 Telefon raqamingizni yozing (masalan: +998901234567)")


def sotuv_yarat(uid):
    h = holat_ol(uid)
    savat = DATA["savatlar"].get(str(uid), [])
    if not savat:
        yubor(uid, "Savat bo'sh.")
        return

    raqam = str(DATA["keyingi_sotuv"])
    DATA["keyingi_sotuv"] += 1

    mahsulotlar = []
    jami = 0
    for x in savat:
        m = DATA["mahsulotlar"].get(x["mahsulot"])
        if not m:
            continue
        summa = int(m.get("narx", 0)) * int(x["soni"])
        jami += summa
        mahsulotlar.append({"id": m["id"], "nom": m["nom"], "olcham": x["olcham"],
                            "soni": x["soni"], "narx": m.get("narx", 0), "summa": summa})
        # zaxiradan ayiramiz
        m["zaxira"][x["olcham"]] = max(0, int(m["zaxira"][x["olcham"]]) - int(x["soni"]))

    usul = h.get("usul", "yetkazish")
    yetkazish = 0 if (jami >= BEPUL_CHEGARA or usul == "olib") else YETKAZISH_NARX

    s = {
        "raqam": raqam,
        "mijoz": int(uid),
        "mahsulotlar": mahsulotlar,
        "jami": jami,
        "yetkazish": yetkazish,
        "umumiy": jami + yetkazish,
        "usul": usul,
        "manzil": h.get("manzil", ""),
        "tel": h.get("tel", ""),
        "holat": "tolov_kutilmoqda",
        "yaratildi": vaqt(),
    }
    DATA["sotuvlar"][raqam] = s
    DATA["savatlar"][str(uid)] = []
    holat_tozala(uid)
    saqla()

    yubor(uid,
          "✅ <b>Buyurtma qabul qilindi!</b>\n\n" + sotuv_matni(s) +
          "\n\n💳 To'lov uchun karta:\n"
          "<code>" + KARTA + "</code>\n" + KARTA_EGASI + "\n\n"
          "To'lagach chek rasmini yuboring 👇",
          kb=tugmalar([[("📸 To'lov chekini yuborish", "schek_" + raqam)]]))

    adminlarga("🛍 <b>Yangi do'kon buyurtmasi</b>\n\n" + sotuv_matni(s, ichki=True))


def sotuv_matni(s, ichki=False):
    q = ["🧾 <b>Buyurtma #" + s["raqam"] + "</b>", ""]
    for m in s["mahsulotlar"]:
        q.append("• " + m["nom"] + " · " + m["olcham"] + " · " + str(m["soni"])
                 + " ta — " + pul(m["summa"]))
    q.append("")
    q.append("💵 Mahsulotlar: " + pul(s["jami"]))
    q.append("🚚 Yetkazish: " + ("bepul" if not s["yetkazish"] else pul(s["yetkazish"])))
    q.append("🧾 <b>Jami: " + pul(s["umumiy"]) + "</b>")
    if s.get("usul") == "olib":
        q.append("\n🏪 O'zi olib ketadi")
    elif s.get("manzil"):
        q.append("\n📍 " + s["manzil"])
    if s.get("tel"):
        q.append("📞 " + s["tel"])
    if ichki:
        q.append("🆔 <code>" + str(s["mijoz"]) + "</code>")
    return "\n".join(q)


def sotuv_holat_ozgartir(raqam, yangi):
    s = DATA["sotuvlar"].get(raqam)
    if not s:
        return
    s["holat"] = yangi
    saqla()
    xabarlar = {
        "tolangan": "✅ To'lovingiz tasdiqlandi! Buyurtmangiz tayyorlanmoqda.",
        "yolda": "🚚 Buyurtmangiz yo'lga chiqdi! Kuryer siz bilan bog'lanadi.",
        "topshirildi": "🎉 Buyurtmangiz topshirildi. Xaridingiz muborak bo'lsin!",
        "bekor": "❌ Buyurtmangiz bekor qilindi. Savol bo'lsa biz bilan bog'laning.",
    }
    if yangi in xabarlar:
        yubor(s["mijoz"], "#" + raqam + " — " + xabarlar[yangi])


def mening_xaridlarim(uid):
    royxat = [s for s in DATA["sotuvlar"].values() if str(s["mijoz"]) == str(uid)]
    if not royxat:
        return None
    nomlar = {"tolov_kutilmoqda": "💳 To'lov kutilmoqda",
              "tekshiruvda": "🔍 Chek tekshirilmoqda",
              "tolangan": "📦 Tayyorlanmoqda", "yolda": "🚚 Yo'lda",
              "topshirildi": "✅ Topshirildi", "bekor": "❌ Bekor"}
    q = ["🛍 <b>Do'kon xaridlaringiz</b>\n"]
    for s in sorted(royxat, key=lambda x: int(x["raqam"]), reverse=True)[:10]:
        q.append("#" + s["raqam"] + " · " + pul(s["umumiy"]) + " · "
                 + nomlar.get(s["holat"], s["holat"]))
    return "\n".join(q)
