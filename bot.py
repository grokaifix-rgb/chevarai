# -*- coding: utf-8 -*-
"""
Chevar AI — hunarmand, mijoz va do'konni bir joyga bog'lovchi Telegram bot.

Uch bo'lim:
  🤖 AI bo'limi     — mijoz oddiy tilda yozadi, bot aniq buyurtma varaqasini
                      tayyorlab hunarmandlarga uzatadi (o'lchov bo'yicha tikish)
  👗 Dizaynlar      — tayyor namunalar, mijoz yoqqanini tanlab o'ziga tiktiradi
  🛍 Do'kon         — o'lchami aniq tayyor mahsulotlar, savat va yetkazib berish

Qo'shimcha kutubxona kerak emas — faqat Python 3.
Ishga tushirish:  python3 bot.py

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

import sys
import time
import traceback

import ai
import admin
import dokon
from core import (ADMINLAR, ALOQA_TEL, ALOQA_TG, BOSH_ADMIN, DATA, KARTA,
                  KARTA_EGASI, OLDINDAN, PLATFORMA, TOKEN, adminlarga, admin_mi,
                  api, holat, holat_ol, holat_tozala, log, menyu_tugmalari,
                  mijoz_narxi, profil, pul, saqla, tahrirla, tasdiqlangan_ustalar,
                  tugmalar, vaqt, yaxlit, yubor, javob_ber, AI_CFG)


# =====================  Menyular  =====================

SALOM = (
    "🧵 <b>" + PLATFORMA + "</b> — milliy tikuvchilik platformasi\n\n"
    "Bu yerda uch xil yo'l bilan kiyim olasiz:\n\n"
    "🤖 <b>AI bilan buyurtma</b> — xohishingizni o'z so'zingiz bilan aytasiz,\n"
    "    bot uni aniq buyurtmaga aylantirib hunarmandga yetkazadi\n\n"
    "👗 <b>Dizaynlar</b> — tayyor namunalardan yoqqanini tanlaysiz,\n"
    "    o'z o'lchamingizga tikib beriladi\n\n"
    "🛍 <b>Do'kon</b> — o'lchami aniq tayyor mahsulotlar,\n"
    "    savatga solib sotib olasiz, uyingizgacha yetkazamiz\n\n"
    "Quyidagi tugmalardan boshlang 👇"
)

MIJOZ_MENYU = menyu_tugmalari([
    ["🤖 AI bilan buyurtma"],
    ["👗 Dizaynlar", "🛍 Do'kon"],
    ["🛒 Savatim", "📦 Buyurtmalarim"],
    ["ℹ️ Yordam", "🪡 Men hunarmandman"],
])

USTA_MENYU = menyu_tugmalari([
    ["📋 Yangi buyurtmalar"],
    ["🧾 Mening ishlarim", "👤 Profilim"],
    ["🛍 Do'kon", "🤖 AI bilan buyurtma"],
])


def menyu(uid):
    return USTA_MENYU if profil(uid).get("rol") == "usta" else MIJOZ_MENYU


YORDAM = (
    "ℹ️ <b>" + PLATFORMA + " qanday ishlaydi</b>\n\n"
    "<b>🤖 AI bilan buyurtma</b>\n"
    "1. Kiyim haqida o'z so'zingiz bilan yozasiz\n"
    "2. Bot savol berib aniq varaqa tayyorlaydi\n"
    "3. Hunarmandlar narx va muddat taklif qiladi\n"
    "4. Siz tanlaysiz, " + str(int(OLDINDAN)) + "% oldindan to'lov\n"
    "5. Tayyor bo'lgach qolgan to'lov\n\n"
    "<b>👗 Dizaynlar</b>\n"
    "Tayyor namunani tanlaysiz, faqat o'lchamingizni berasiz\n\n"
    "<b>🛍 Do'kon</b>\n"
    "Tayyor mahsulot — o'lcham tanlaysiz, savatga solasiz,\n"
    "to'laysiz va manzilingizga yetkaziladi\n\n"
    "📞 Aloqa: " + ALOQA_TEL + " · " + ALOQA_TG + "\n"
    "Buyruqlar: /start /buyurtma /dizayn /dokon /savat /usta /yordam"
)


# =====================  AI BO'LIMI: buyurtma yig'ish  =====================

def buyurtma_boshla(uid):
    holat(uid, "suhbat", suhbat=[], buyurtma={}, savollar=0)
    saqla()
    yubor(uid,
          "🤖 <b>AI bilan buyurtma</b>\n\n"
          "Qanday kiyim kerakligini o'z so'zingiz bilan yozing.\n"
          "Mato, rang, fason yoki qaysi tadbirga kerakligini aytsangiz — "
          "yanada aniq bo'ladi.\n\n"
          "<i>Masalan: «To'yga ko'k adras matodan zamonaviy ko'ylak kerak»</i>\n\n"
          "<i>Bekor qilish uchun /bekor</i>")


def suhbat_davom(uid, matn):
    h = holat(uid)
    suhbat = h.get("suhbat", [])
    suhbat.append({"rol": "mijoz", "matn": matn})

    yubor(uid, "🤖 <i>O'ylayapman...</i>")
    natija = ai.tahlil(AI_CFG, suhbat)

    h["buyurtma"] = natija.get("buyurtma") or {}
    savol_soni = h.get("savollar", 0)

    if not natija.get("tayyor") and natija.get("savol") and savol_soni < 4:
        savol = natija["savol"]
        suhbat.append({"rol": "ai", "matn": savol})
        h["suhbat"] = suhbat
        h["savollar"] = savol_soni + 1
        saqla()
        yubor(uid, "❓ " + savol)
        return

    h["suhbat"] = suhbat
    saqla()
    varaqa_korsat(uid)


def varaqa_korsat(uid):
    b = holat_ol(uid).get("buyurtma", {})
    yubor(uid, "📝 <b>Buyurtma varaqasi</b>\n\n" + ai.varaqa(b) + "\n\nHammasi to'g'rimi?",
          kb=tugmalar([
              [("✅ To'g'ri, davom etamiz", "v_ok")],
              [("✏️ O'zgartiraman", "v_tahrir")],
              [("❌ Bekor qilish", "v_bekor")],
          ]))


OLCHAM_SAVOLLARI = [
    ("boy", "📏 Bo'yingiz necha sm? (masalan: 165)"),
    ("kokrak", "📏 Ko'krak aylanasi necha sm? (bilmasangiz «-» yozing)"),
    ("bel", "📏 Bel aylanasi necha sm? (bilmasangiz «-» yozing)"),
    ("son", "📏 Son (dumba) aylanasi necha sm? (bilmasangiz «-» yozing)"),
]


def olcham_sora(uid, indeks=0):
    if indeks >= len(OLCHAM_SAVOLLARI):
        holat(uid, "muddat")
        saqla()
        yubor(uid, "🗓 Buyurtma qachonga kerak? "
                   "(masalan: «2 hafta ichida» yoki «15-oktabrga»)")
        return
    kalit, savol = OLCHAM_SAVOLLARI[indeks]
    holat(uid, "olcham", olcham_indeks=indeks)
    saqla()
    yubor(uid, savol)


def buyurtma_yarat(uid):
    h = holat_ol(uid)
    raqam = str(DATA["keyingi_raqam"])
    DATA["keyingi_raqam"] += 1

    b = {
        "raqam": raqam,
        "mijoz": int(uid),
        "mijoz_ism": profil(uid).get("ism") or "",
        "mijoz_tel": h.get("tel", ""),
        "tafsilot": h.get("buyurtma", {}),
        "olcham": h.get("olcham", {}),
        "muddat": h.get("muddat", ""),
        "dizayn": h.get("dizayn", ""),
        "dizayn_rasm": h.get("dizayn_rasm", ""),
        "holat": "yangi",
        "takliflar": {},
        "usta": None,
        "usta_narx": 0,
        "umumiy_narx": 0,
        "tolov": {"oldindan": 0, "qolgan": 0, "holat": "kutilmoqda"},
        "yaratildi": vaqt(),
        "tarix": [],
    }
    DATA["buyurtmalar"][raqam] = b
    holat_tozala(uid)
    saqla()

    yubor(uid,
          "✅ <b>Buyurtma qabul qilindi!</b>\n\n"
          "Raqami: <b>#" + raqam + "</b>\n\n" + buyurtma_matni(b) +
          "\n\n🪡 Buyurtmangiz hunarmandlarga yuborildi.\n"
          "Ular narx va muddat taklif qilishadi — tez orada xabar beramiz.",
          menyu=menyu(uid))

    ustalarga_yubor(b)
    adminlarga("🆕 Yangi tikish buyurtmasi <b>#" + raqam + "</b>\n\n"
               + buyurtma_matni(b, ichki=True))


def buyurtma_matni(b, ichki=False):
    q = ["📝 <b>Buyurtma #" + b["raqam"] + "</b>", "", ai.varaqa(b.get("tafsilot", {}))]
    o = b.get("olcham") or {}
    nomlar = {"boy": "Bo'y", "kokrak": "Ko'krak", "bel": "Bel", "son": "Son"}
    olch = [nom + ": " + str(o[k]) for k, nom in nomlar.items()
            if o.get(k) and o[k] != "-"]
    if olch:
        q.append("\n📏 <b>O'lchamlar:</b> " + ", ".join(olch))
    if b.get("muddat"):
        q.append("🗓 <b>Muddat:</b> " + b["muddat"])
    if b.get("dizayn"):
        q.append("👗 <b>Namuna kodi:</b> " + b["dizayn"])
    if ichki and b.get("mijoz_tel"):
        q.append("📞 <b>Mijoz:</b> " + b["mijoz_tel"])
    return "\n".join(q)


def ustalarga_yubor(b):
    ustalar = tasdiqlangan_ustalar()
    if not ustalar:
        adminlarga("⚠️ Tasdiqlangan hunarmand yo'q — #" + b["raqam"]
                   + " buyurtmasi hech kimga yuborilmadi.")
        return
    matn = ("🆕 <b>Yangi buyurtma</b>\n\n" + buyurtma_matni(b) +
            "\n\n💡 Narxingizni <b>o'z xarajatingiz + mehnatingiz</b> bo'yicha kiriting.\n"
            "Platforma o'z ustamasini alohida qo'shadi.")
    kb = tugmalar([[("💰 Narx taklif qilish", "n_" + b["raqam"])],
                   [("⏭ O'tkazib yuborish", "skip_" + b["raqam"])]])
    for uid in ustalar:
        if b.get("dizayn_rasm"):
            from core import rasm_yubor
            rasm_yubor(int(uid), b["dizayn_rasm"], matn, kb)
        else:
            yubor(int(uid), matn, kb=kb)


# =====================  HUNARMAND  =====================

USTA_SAVOLLARI = [
    ("ism", "👤 Ism-familiyangizni yozing:"),
    ("shahar", "📍 Qaysi shahar/tumandasiz?"),
    ("ixtisos", "🪡 Nima tikasiz? (masalan: milliy ko'ylak, chapan, kostyum)"),
    ("tajriba", "⏳ Necha yil tajribangiz bor?"),
    ("tel", "📞 Telefon raqamingiz (masalan: +998901234567):"),
]


def usta_royxat_boshla(uid):
    p = profil(uid)
    if p.get("rol") == "usta" and p.get("tasdiq"):
        yubor(uid, "✅ Siz allaqachon tasdiqlangan hunarmandsiz.", menyu=USTA_MENYU)
        return
    if p.get("rol") == "usta" and not p.get("tasdiq"):
        yubor(uid, "⏳ Arizangiz ko'rib chiqilmoqda. Tasdiqlangach xabar beramiz.")
        return
    holat(uid, "usta_reg", usta_indeks=0, usta={})
    saqla()
    yubor(uid, "🪡 <b>Hunarmand sifatida ro'yxatdan o'tish</b>\n\n"
               "Bir necha savolga javob bering.\n<i>Bekor qilish: /bekor</i>\n\n"
               + USTA_SAVOLLARI[0][1])


def usta_reg_davom(uid, matn):
    h = holat_ol(uid)
    i = h.get("usta_indeks", 0)
    h.setdefault("usta", {})[USTA_SAVOLLARI[i][0]] = matn.strip()
    i += 1
    if i < len(USTA_SAVOLLARI):
        h["usta_indeks"] = i
        saqla()
        yubor(uid, USTA_SAVOLLARI[i][1])
        return

    p = profil(uid)
    p.update(h["usta"])
    p["rol"] = "usta"
    p["tasdiq"] = False
    holat_tozala(uid)
    saqla()

    yubor(uid, "✅ Arizangiz yuborildi!\n\n"
               "Administrator tekshirib chiqadi (odatda 1 kun ichida).\n"
               "Tasdiqlangach, yangi buyurtmalar sizga avtomatik kelib turadi.",
          menyu=MIJOZ_MENYU)

    adminlarga("🪡 <b>Yangi hunarmand arizasi</b>\n\n"
               "👤 " + p.get("ism", "") + "\n📍 " + p.get("shahar", "") + "\n"
               "🪡 " + p.get("ixtisos", "") + "\n⏳ Tajriba: " + str(p.get("tajriba", "")) + "\n"
               "📞 " + p.get("tel", "") + "\n🆔 <code>" + str(uid) + "</code>",
               kb=tugmalar([[("✅ Tasdiqlash", "utasdiq_" + str(uid)),
                             ("❌ Rad etish", "urad_" + str(uid))]]))


def narx_sora(uid, raqam):
    b = DATA["buyurtmalar"].get(raqam)
    if not b or b["holat"] != "yangi":
        yubor(uid, "Bu buyurtma allaqachon yopilgan.")
        return
    holat(uid, "narx", narx_raqam=raqam)
    saqla()
    yubor(uid, "💰 <b>#" + raqam + "</b> uchun narxingizni yozing (faqat son, so'mda).\n"
               "<i>Masalan: 500000</i>\n\nBekor qilish: /bekor")


def narx_qabul(uid, matn):
    son = "".join(c for c in matn if c.isdigit())
    if not son or int(son) < 10000:
        yubor(uid, "❗️ Narxni to'g'ri kiriting (kamida 10000). Masalan: 500000")
        return
    holat(uid, "narx_kun", narx_qiymat=int(son))
    saqla()
    yubor(uid, "🗓 Necha kunda tikib berasiz? (faqat son, masalan: 10)")


def kun_qabul(uid, matn):
    h = holat_ol(uid)
    raqam = h.get("narx_raqam")
    kun = "".join(c for c in matn if c.isdigit())
    if not kun:
        yubor(uid, "❗️ Kunlar sonini raqamda yozing. Masalan: 10")
        return

    b = DATA["buyurtmalar"].get(raqam)
    if not b or b["holat"] != "yangi":
        holat_tozala(uid)
        saqla()
        yubor(uid, "Bu buyurtma allaqachon yopilgan.", menyu=USTA_MENYU)
        return

    usta_narx = h["narx_qiymat"]
    b["takliflar"][str(uid)] = {"narx": usta_narx, "mijoz_narx": mijoz_narxi(usta_narx),
                                "kun": int(kun), "vaqt": vaqt()}
    holat_tozala(uid)
    saqla()

    yubor(uid, "✅ Taklifingiz yuborildi!\n\nSizning narxingiz: <b>" + pul(usta_narx)
          + "</b>\nMuddat: <b>" + kun + " kun</b>\n\n"
          "Mijoz tanlasa — darhol xabar beramiz.", menyu=USTA_MENYU)

    p = profil(uid)
    yubor(b["mijoz"],
          "💰 <b>#" + raqam + " uchun yangi taklif!</b>\n\n"
          "🪡 Hunarmand: <b>" + (p.get("ism") or "Hunarmand") + "</b>"
          + (" (" + p.get("shahar", "") + ")" if p.get("shahar") else "") + "\n"
          "🧵 Ixtisos: " + (p.get("ixtisos") or "-") + "\n"
          "💵 Narx: <b>" + pul(mijoz_narxi(usta_narx)) + "</b>\n"
          "🗓 Muddat: <b>" + kun + " kun</b>\n\nBu taklifni qabul qilasizmi?",
          kb=tugmalar([
              [("✅ Qabul qilaman", "tanla_" + raqam + "_" + str(uid))],
              [("👀 Boshqa takliflarni kutaman", "kut_" + raqam)],
          ]))


def usta_tanlandi(mijoz_uid, raqam, usta_uid):
    b = DATA["buyurtmalar"].get(raqam)
    if not b or b["holat"] != "yangi":
        yubor(mijoz_uid, "Bu buyurtma bo'yicha hunarmand allaqachon tanlangan.")
        return
    taklif = b["takliflar"].get(str(usta_uid))
    if not taklif:
        yubor(mijoz_uid, "Taklif topilmadi.")
        return

    b["usta"] = int(usta_uid)
    b["usta_narx"] = taklif["narx"]
    b["umumiy_narx"] = taklif["mijoz_narx"]
    b["muddat_kun"] = taklif["kun"]
    b["holat"] = "tasdiqlangan"
    b["tolov"]["oldindan"] = yaxlit(taklif["mijoz_narx"] * OLDINDAN / 100.0, 1000)
    b["tolov"]["qolgan"] = taklif["mijoz_narx"] - b["tolov"]["oldindan"]
    b["tarix"].append(vaqt() + " — hunarmand tanlandi")
    saqla()

    yubor(mijoz_uid,
          "🎉 <b>Ajoyib! Hunarmand biriktirildi.</b>\n\n"
          "Buyurtma: <b>#" + raqam + "</b>\n"
          "Umumiy narx: <b>" + pul(b["umumiy_narx"]) + "</b>\n"
          "Muddat: <b>" + str(taklif["kun"]) + " kun</b>\n\n"
          "💳 Ishni boshlash uchun oldindan to'lov (" + str(int(OLDINDAN)) + "%): "
          "<b>" + pul(b["tolov"]["oldindan"]) + "</b>\n\n"
          "Karta: <code>" + KARTA + "</code>\n"
          "Egasi: " + KARTA_EGASI + "\n\nTo'lagach, chek rasmini yuboring 👇",
          kb=tugmalar([[("📸 To'lov chekini yuborish", "chek_" + raqam)],
                       [("❌ Buyurtmani bekor qilish", "bekor_" + raqam)]]))

    yubor(int(usta_uid),
          "🎉 <b>Sizning taklifingiz qabul qilindi!</b>\n\n"
          + buyurtma_matni(b, ichki=True) +
          "\n💵 Sizga to'lanadi: <b>" + pul(b["usta_narx"]) + "</b>\n"
          "🗓 Muddat: " + str(taklif["kun"]) + " kun\n\n"
          "⏳ Mijoz oldindan to'lov qilgach, ishni boshlashga signal beramiz.")

    for u in b["takliflar"]:
        if str(u) != str(usta_uid):
            yubor(int(u), "ℹ️ #" + raqam + " buyurtmasi bo'yicha boshqa hunarmand "
                          "tanlandi. Keyingi buyurtmalarda omad!")


# =====================  TO'LOV (tikish buyurtmalari)  =====================

def chek_sora(uid, raqam, tur="oldindan"):
    holat(uid, "chek", chek_raqam=raqam, chek_tur=tur)
    saqla()
    yubor(uid, "📸 To'lov chekining rasmini (yoki skrinshotini) shu yerga yuboring.")


def chek_qabul(uid, msg):
    h = holat_ol(uid)
    raqam = h.get("chek_raqam")
    tur = h.get("chek_tur", "oldindan")
    b = DATA["buyurtmalar"].get(raqam)
    holat_tozala(uid)
    if not b:
        saqla()
        return
    b["tolov"]["holat"] = ("oldindan_tekshiruvda" if tur == "oldindan"
                           else "qolgan_tekshiruvda")
    saqla()
    yubor(uid, "✅ Chek qabul qilindi. Tekshirilgach xabar beramiz.", menyu=menyu(uid))

    summa = b["tolov"]["oldindan"] if tur == "oldindan" else b["tolov"]["qolgan"]
    for a in ADMINLAR:
        api("forwardMessage", chat_id=a, from_chat_id=uid, message_id=msg["message_id"])
        yubor(a, "💳 <b>To'lov cheki</b> — #" + raqam + "\n"
                 "Tur: " + ("oldindan" if tur == "oldindan" else "yakuniy") + "\n"
                 "Summa: <b>" + pul(summa) + "</b>\n"
                 "Mijoz: <code>" + str(uid) + "</code>",
              kb=tugmalar([[("✅ To'lov tasdiqlandi", "tol_" + raqam + "_" + tur),
                            ("❌ Rad", "tolrad_" + raqam + "_" + tur)]]))


def sotuv_chek_qabul(uid, msg):
    h = holat_ol(uid)
    raqam = h.get("schek_raqam")
    s = DATA["sotuvlar"].get(raqam)
    holat_tozala(uid)
    if not s:
        saqla()
        return
    s["holat"] = "tekshiruvda"
    saqla()
    yubor(uid, "✅ Chek qabul qilindi. Tekshirilgach buyurtmangiz jo'natiladi.",
          menyu=menyu(uid))
    for a in ADMINLAR:
        api("forwardMessage", chat_id=a, from_chat_id=uid, message_id=msg["message_id"])
        yubor(a, "💳 <b>Do'kon to'lovi</b> — #" + raqam + "\n"
                 "Summa: <b>" + pul(s["umumiy"]) + "</b>\n"
                 "Mijoz: <code>" + str(uid) + "</code>",
              kb=tugmalar([[("✅ To'lovni tasdiqlash", "stol_" + raqam),
                            ("❌ Bekor", "sbekor_" + raqam)]]))


def tolov_tasdiq(raqam, tur):
    b = DATA["buyurtmalar"].get(raqam)
    if not b:
        return
    if tur == "oldindan":
        b["holat"] = "tikilmoqda"
        b["tolov"]["holat"] = "oldindan_tolangan"
        b["tarix"].append(vaqt() + " — oldindan to'lov qabul qilindi")
        saqla()
        yubor(b["mijoz"], "✅ To'lovingiz tasdiqlandi!\n\n"
                          "🪡 Hunarmand ishni boshladi. Tayyor bo'lgach xabar beramiz.")
        if b.get("usta"):
            yubor(b["usta"], "🟢 <b>#" + raqam + " — ishni boshlang!</b>\n\n"
                             "Mijoz oldindan to'lovni amalga oshirdi.\n"
                             + buyurtma_matni(b, ichki=True),
                  kb=tugmalar([[("✅ Tayyor bo'ldi", "tayyor_" + raqam)]]))
    else:
        b["holat"] = "yakunlandi"
        b["tolov"]["holat"] = "toliq_tolangan"
        b["tarix"].append(vaqt() + " — yakuniy to'lov qabul qilindi")
        saqla()
        yubor(b["mijoz"], "🎉 Buyurtma yakunlandi! Xizmatimizdan foydalanganingiz "
                          "uchun rahmat.\n\nHunarmandni baholang:",
              kb=tugmalar([[("⭐️" * i, "baho_" + raqam + "_" + str(i))] for i in (5, 4, 3)]))
        if b.get("usta"):
            yubor(b["usta"], "💰 <b>#" + raqam + "</b> yakunlandi. Sizning ulushingiz: <b>"
                  + pul(b["usta_narx"]) + "</b>\nHisob-kitob administrator orqali.")


def ish_tayyor(usta_uid, raqam):
    b = DATA["buyurtmalar"].get(raqam)
    if not b or str(b.get("usta")) != str(usta_uid):
        return
    b["holat"] = "tayyor"
    b["tarix"].append(vaqt() + " — hunarmand ishni tayyor dedi")
    saqla()
    yubor(usta_uid, "✅ Rahmat! Mijozga xabar berdik.")
    yubor(b["mijoz"],
          "🎊 <b>Buyurtmangiz tayyor!</b> (#" + raqam + ")\n\n"
          "Qolgan to'lov: <b>" + pul(b["tolov"]["qolgan"]) + "</b>\n"
          "Karta: <code>" + KARTA + "</code>\nEgasi: " + KARTA_EGASI + "\n\n"
          "To'lagach chekni yuboring — so'ng yetkazib berish kelishiladi.",
          kb=tugmalar([[("📸 Yakuniy to'lov cheki", "chek2_" + raqam)]]))


# =====================  RO'YXATLAR  =====================

HOLAT_NOMI = {
    "yangi": "🕐 Takliflar kutilmoqda",
    "tasdiqlangan": "💳 Oldindan to'lov kutilmoqda",
    "tikilmoqda": "🪡 Tikilmoqda",
    "tayyor": "🎊 Tayyor — yakuniy to'lov",
    "yakunlandi": "✅ Yakunlandi",
    "bekor": "❌ Bekor qilingan",
}


def mijoz_buyurtmalari(uid):
    royxat = [b for b in DATA["buyurtmalar"].values() if str(b["mijoz"]) == str(uid)]
    qismlar = []
    if royxat:
        q = ["🤖 <b>Tikish buyurtmalari</b>\n"]
        for b in sorted(royxat, key=lambda x: int(x["raqam"]), reverse=True)[:10]:
            tur = b.get("tafsilot", {}).get("kiyim") or "buyurtma"
            satr = "#" + b["raqam"] + " — " + tur + " · " + HOLAT_NOMI.get(b["holat"], b["holat"])
            if b.get("umumiy_narx"):
                satr += " · " + pul(b["umumiy_narx"])
            if b["holat"] == "yangi" and b["takliflar"]:
                satr += " (" + str(len(b["takliflar"])) + " ta taklif)"
            q.append(satr)
        qismlar.append("\n".join(q))

    xarid = dokon.mening_xaridlarim(uid)
    if xarid:
        qismlar.append(xarid)

    if not qismlar:
        yubor(uid, "📦 Sizda hali buyurtma yo'q.\n\n"
                   "«🤖 AI bilan buyurtma» yoki «🛍 Do'kon» dan boshlang.",
              menyu=menyu(uid))
        return
    yubor(uid, "\n\n".join(qismlar), menyu=menyu(uid))


def usta_buyurtmalari(uid):
    ochiq = [b for b in DATA["buyurtmalar"].values()
             if b["holat"] == "yangi" and str(uid) not in b["takliflar"]]
    if not ochiq:
        yubor(uid, "📋 Hozircha yangi buyurtma yo'q. Yangisi kelsa darhol yuboramiz.",
              menyu=USTA_MENYU)
        return
    for b in sorted(ochiq, key=lambda x: int(x["raqam"]), reverse=True)[:5]:
        yubor(uid, "🆕 " + buyurtma_matni(b),
              kb=tugmalar([[("💰 Narx taklif qilish", "n_" + b["raqam"])]]))


def usta_ishlari(uid):
    royxat = [b for b in DATA["buyurtmalar"].values() if str(b.get("usta")) == str(uid)]
    if not royxat:
        yubor(uid, "🧾 Sizda hali qabul qilingan ish yo'q.", menyu=USTA_MENYU)
        return
    q = ["🧾 <b>Sizning ishlaringiz</b>\n"]
    jami = 0
    for b in sorted(royxat, key=lambda x: int(x["raqam"]), reverse=True)[:15]:
        q.append("#" + b["raqam"] + " — " + pul(b["usta_narx"]) + " · "
                 + HOLAT_NOMI.get(b["holat"], b["holat"]))
        if b["holat"] == "yakunlandi":
            jami += b["usta_narx"]
    q.append("\n💰 Yakunlangan ishlardan jami: <b>" + pul(jami) + "</b>")
    yubor(uid, "\n".join(q), menyu=USTA_MENYU)


def usta_profil(uid):
    p = profil(uid)
    baholar = p.get("baholar", [])
    ort = (sum(baholar) / len(baholar)) if baholar else 0
    yubor(uid,
          "👤 <b>Profilingiz</b>\n\n"
          "Ism: " + (p.get("ism") or "-") + "\n"
          "Shahar: " + (p.get("shahar") or "-") + "\n"
          "Ixtisos: " + (p.get("ixtisos") or "-") + "\n"
          "Tajriba: " + str(p.get("tajriba") or "-") + " yil\n"
          "Telefon: " + (p.get("tel") or "-") + "\n"
          "Holat: " + ("✅ tasdiqlangan" if p.get("tasdiq") else "⏳ kutilmoqda") + "\n"
          "Reyting: " + (("⭐️ %.1f (%d baho)" % (ort, len(baholar))) if baholar else "hali yo'q"),
          menyu=USTA_MENYU)


# =====================  XABARLARNI MARSHRUTLASH  =====================

def xabar(msg):
    if msg.get("chat", {}).get("type") != "private":
        return
    uid = msg["from"]["id"]
    p = profil(uid)
    if p.get("bloklangan"):
        return
    if not p.get("ism"):
        p["ism"] = (msg["from"].get("first_name", "") + " "
                    + msg["from"].get("last_name", "")).strip()

    h = holat_ol(uid)
    bosqich = h.get("bosqich", "")

    # --- Rasm keldi ---
    if "photo" in msg or "document" in msg:
        file_id = msg["photo"][-1]["file_id"] if "photo" in msg else ""
        if bosqich == "chek":
            chek_qabul(uid, msg)
            return
        if bosqich == "schek":
            sotuv_chek_qabul(uid, msg)
            return
        if bosqich == "qosh_rasm" and admin_mi(uid):
            admin.rasm_qabul(uid, file_id)
            return

    matn = (msg.get("text") or "").strip()
    if not matn:
        if bosqich in ("chek", "schek", "qosh_rasm"):
            yubor(uid, "📸 Iltimos, <b>rasm</b> yuboring.")
        return

    past = matn.lower()

    # --- Buyruqlar ---
    if past.startswith("/start"):
        holat_tozala(uid)
        saqla()
        yubor(uid, SALOM, menyu=menyu(uid))
        return
    if past.startswith("/bekor"):
        holat_tozala(uid)
        saqla()
        yubor(uid, "❌ Bekor qilindi.", menyu=menyu(uid))
        return
    if past.startswith("/otkaz") and bosqich == "qosh_rasm":
        admin.rasm_qabul(uid, "")
        return
    if past.startswith("/yordam") or matn == "ℹ️ Yordam":
        yubor(uid, YORDAM, menyu=menyu(uid))
        return
    if past.startswith("/admin"):
        if admin_mi(uid):
            admin.panel(uid)
        return
    if past.startswith("/ochir") and admin_mi(uid):
        admin.ochir(uid, matn[6:].strip())
        return
    if past.startswith("/usta") or matn == "🪡 Men hunarmandman":
        usta_royxat_boshla(uid)
        return
    if past.startswith("/buyurtma") or matn == "🤖 AI bilan buyurtma":
        buyurtma_boshla(uid)
        return
    if past.startswith("/dizayn") or matn == "👗 Dizaynlar":
        dokon.dizaynlar_royxati(uid)
        return
    if past.startswith("/dokon") or matn == "🛍 Do'kon":
        dokon.dokon_kategoriyalar(uid)
        return
    if past.startswith("/savat") or matn == "🛒 Savatim":
        dokon.savat_korsat(uid)
        return
    if matn == "📦 Buyurtmalarim":
        mijoz_buyurtmalari(uid)
        return
    if matn == "📋 Yangi buyurtmalar":
        usta_buyurtmalari(uid)
        return
    if matn == "🧾 Mening ishlarim":
        usta_ishlari(uid)
        return
    if matn == "👤 Profilim":
        usta_profil(uid)
        return

    # --- Bosqichlar ---
    if bosqich == "suhbat":
        suhbat_davom(uid, matn)
    elif bosqich == "olcham":
        i = h.get("olcham_indeks", 0)
        h.setdefault("olcham", {})[OLCHAM_SAVOLLARI[i][0]] = matn
        saqla()
        olcham_sora(uid, i + 1)
    elif bosqich == "muddat":
        h["muddat"] = matn
        holat(uid, "tel")
        saqla()
        yubor(uid, "📞 Aloqa uchun telefon raqamingizni yozing "
                   "(masalan: +998901234567)")
    elif bosqich == "tel":
        if len(matn.replace(" ", "")) < 7:
            yubor(uid, "❗️ Telefon raqamni to'liq yozing.")
            return
        h["tel"] = matn.replace(" ", "")
        saqla()
        buyurtma_yarat(uid)
    elif bosqich == "usta_reg":
        usta_reg_davom(uid, matn)
    elif bosqich == "narx":
        narx_qabul(uid, matn)
    elif bosqich == "narx_kun":
        kun_qabul(uid, matn)
    elif bosqich == "qosh" and admin_mi(uid):
        admin.qoshish_davom(uid, matn)
    elif bosqich == "sotuv_manzil":
        h["manzil"] = matn
        holat(uid, "sotuv_tel")
        saqla()
        yubor(uid, "📞 Telefon raqamingizni yozing (masalan: +998901234567)")
    elif bosqich == "sotuv_tel":
        if len(matn.replace(" ", "")) < 7:
            yubor(uid, "❗️ Telefon raqamni to'liq yozing.")
            return
        h["tel"] = matn.replace(" ", "")
        saqla()
        dokon.sotuv_yarat(uid)
    elif len(matn) > 8:
        # Bosqich yo'q: erkin matnni buyurtma deb qabul qilamiz
        holat(uid, "suhbat", suhbat=[], buyurtma={}, savollar=0)
        saqla()
        suhbat_davom(uid, matn)
    else:
        yubor(uid, SALOM, menyu=menyu(uid))


def tugma(cq):
    uid = cq["from"]["id"]
    data = cq.get("data", "")
    msg = cq.get("message", {})
    message_id = msg.get("message_id")
    javob_ber(cq["id"])

    # --- AI buyurtma varaqasi ---
    if data == "v_ok":
        h = holat_ol(uid)
        if not h.get("buyurtma"):
            buyurtma_boshla(uid)
            return
        h["olcham"] = {}
        saqla()
        yubor(uid, "📏 Endi o'lchamlaringizni olamiz (aniq tikilishi uchun).")
        olcham_sora(uid, 0)
        return
    if data == "v_tahrir":
        holat(uid, "suhbat")
        saqla()
        yubor(uid, "✏️ Nimani o'zgartiramiz? O'zgartirishni yozing.")
        return
    if data == "v_bekor":
        holat_tozala(uid)
        saqla()
        yubor(uid, "❌ Buyurtma bekor qilindi.", menyu=menyu(uid))
        return

    # --- Hunarmand ---
    if data.startswith("n_"):
        narx_sora(uid, data[2:])
        return
    if data.startswith("skip_"):
        tahrirla(uid, message_id, "⏭ O'tkazib yuborildi.")
        return
    if data.startswith("tanla_"):
        _, raqam, usta_uid = data.split("_", 2)
        usta_tanlandi(uid, raqam, usta_uid)
        return
    if data.startswith("kut_"):
        yubor(uid, "👌 Yaxshi, boshqa takliflar kelishini kutamiz.")
        return
    if data.startswith("tayyor_"):
        ish_tayyor(uid, data[7:])
        return

    # --- To'lov ---
    if data.startswith("chek2_"):
        chek_sora(uid, data[6:], "qolgan")
        return
    if data.startswith("chek_"):
        chek_sora(uid, data[5:], "oldindan")
        return
    if data.startswith("schek_"):
        holat(uid, "schek", schek_raqam=data[6:])
        saqla()
        yubor(uid, "📸 To'lov chekining rasmini yuboring.")
        return

    if data.startswith("bekor_"):
        raqam = data[6:]
        b = DATA["buyurtmalar"].get(raqam)
        if b and str(b["mijoz"]) == str(uid) and b["holat"] in ("yangi", "tasdiqlangan"):
            b["holat"] = "bekor"
            saqla()
            yubor(uid, "❌ Buyurtma #" + raqam + " bekor qilindi.", menyu=menyu(uid))
            if b.get("usta"):
                yubor(b["usta"], "ℹ️ Mijoz #" + raqam + " buyurtmasini bekor qildi.")
        return

    if data.startswith("baho_"):
        _, raqam, ball = data.split("_")
        b = DATA["buyurtmalar"].get(raqam)
        if b and b.get("usta"):
            profil(b["usta"]).setdefault("baholar", []).append(int(ball))
            b["baho"] = int(ball)
            saqla()
            yubor(uid, "🙏 Bahoyingiz uchun rahmat!")
            yubor(b["usta"], "⭐️ Sizga yangi baho: " + "⭐️" * int(ball))
        return

    # --- Dizaynlar va do'kon ---
    if data.startswith("dzsah_"):
        dokon.dizaynlar_royxati(uid, int(data[6:]))
        return
    if data.startswith("dz_"):
        dokon.dizayn_tanlandi(uid, data[3:])
        return
    if data == "dokon":
        dokon.dokon_kategoriyalar(uid)
        return
    if data.startswith("kat_"):
        dokon.mahsulotlar_royxati(uid, data[4:])
        return
    if data.startswith("mh_"):
        dokon.olcham_tanlash(uid, data[3:])
        return
    if data.startswith("olch_"):
        _, mahsulot, olcham = data.split("_", 2)
        dokon.savatga_qosh(uid, mahsulot, olcham)
        return
    if data == "savat":
        dokon.savat_korsat(uid)
        return
    if data == "savat_toza":
        DATA["savatlar"][str(uid)] = []
        saqla()
        yubor(uid, "🗑 Savat bo'shatildi.")
        return
    if data.startswith(("kam_", "kop_", "och_")):
        dokon.savat_ozgartir(uid, int(data.split("_")[1]), data.split("_")[0])
        return
    if data == "rasmiy":
        dokon.rasmiylashtirish_boshla(uid)
        return
    if data.startswith("us_"):
        dokon.usul_tanlandi(uid, data[3:])
        return
    if data == "hech":
        return

    # --- Admin tugmalari ---
    admin.tugma(uid, data, message_id)


# =====================  ASOSIY SIKL  =====================

def main():
    if not TOKEN:
        print("\n❗️ Bot tokeni topilmadi.\n"
              "Uy kompyuterida: SOZLASH.command orqali kiriting.\n"
              "Serverda: BOT_TOKEN muhit o'zgaruvchisini qo'ying.\n")
        sys.exit(1)
    if not ADMINLAR:
        print("\n❗️ Admin ID ko'rsatilmagan (ADMIN_IDS yoki config.json).\n")
        sys.exit(1)

    me = api("getMe")
    if not me or not me.get("ok"):
        print("❗️ Token noto'g'ri yoki internet yo'q.")
        sys.exit(1)
    nom = me["result"].get("username")
    log("Bot ishga tushdi: @" + str(nom) + " · adminlar: " + str(ADMINLAR))
    log("Baza: " + str(len(DATA["foydalanuvchilar"])) + " foydalanuvchi, "
        + str(len(DATA["buyurtmalar"])) + " tikish buyurtmasi, "
        + str(len(DATA["sotuvlar"])) + " do'kon buyurtmasi, "
        + str(len(DATA["mahsulotlar"])) + " mahsulot, "
        + str(len(DATA["dizaynlar"])) + " dizayn")

    api("setMyCommands", commands=[
        {"command": "start", "description": "Boshlash"},
        {"command": "buyurtma", "description": "AI bilan buyurtma berish"},
        {"command": "dizayn", "description": "Tayyor dizaynlar"},
        {"command": "dokon", "description": "Do'kon — tayyor mahsulotlar"},
        {"command": "savat", "description": "Savatim"},
        {"command": "usta", "description": "Hunarmand bo'lib ro'yxatdan o'tish"},
        {"command": "yordam", "description": "Yordam"},
        {"command": "bekor", "description": "Joriy amalni bekor qilish"},
    ])

    for a in ADMINLAR:
        yubor(a, "🟢 " + PLATFORMA + " boti ishga tushdi (@" + str(nom) + ")")

    while True:
        try:
            r = api("getUpdates", offset=DATA["offset"] + 1, timeout=50,
                    allowed_updates=["message", "callback_query"])
            if not r or not r.get("ok"):
                time.sleep(3)
                continue
            for u in r["result"]:
                DATA["offset"] = u["update_id"]
                try:
                    if "message" in u:
                        xabar(u["message"])
                    elif "callback_query" in u:
                        tugma(u["callback_query"])
                except Exception:
                    log("Xatolik:\n" + traceback.format_exc())
                saqla()
        except KeyboardInterrupt:
            log("Bot to'xtatildi.")
            saqla()
            break
        except Exception:
            log("Sikl xatosi:\n" + traceback.format_exc())
            time.sleep(5)


if __name__ == "__main__":
    main()
