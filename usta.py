# -*- coding: utf-8 -*-
"""
Chevar AI — hunarmand (tikuvchi) imkoniyatlari:
  🖼 Portfolio — o'z ishlarining rasmlari (mijoz taklif bilan birga ko'radi)
  ⏸ Dam olish rejimi — vaqtincha yangi buyurtma olmaslik
  ✏️ Profilni tahrirlash
  ✉️ Mijoz bilan bot orqali yozishish (telefon raqamni oshkor qilmasdan)
  📸 Tayyor ishning rasmi bilan topshirish

Muallif: Mirzabek Shukurullayev · Tel: +998910964410 · Telegram: @diumuser
"""

from core import (DATA, api, esc, holat, holat_ol, holat_tozala, profil,
                  rasm_yubor, saqla, tugmalar, usta_reyting, vaqt, yubor)

PORTFOLIO_MAX = 10
FAOL_HOLATLAR = ("tasdiqlangan", "tikilmoqda", "tayyor")


def reyting_matni(uid):
    ort, soni, yakun = usta_reyting(uid)
    q = []
    if soni:
        q.append("⭐️ %.1f (%d baho)" % (ort, soni))
    else:
        q.append("⭐️ hali baho yo'q")
    q.append("✅ " + str(yakun) + " ta bajarilgan ish")
    return " · ".join(q)


# =====================  PORTFOLIO  =====================

def portfolio_menyu(uid):
    p = profil(uid)
    rasmlar = p.get("portfolio", [])
    yubor(uid,
          "🖼 <b>Portfolio</b>\n\n"
          "Bu yerga o'zingiz tikkan kiyimlarning rasmlarini qo'ying.\n"
          "Mijoz sizning taklifingizni ko'rganda shu rasmlarni ham ko'radi —\n"
          "yaxshi rasmlar tanlanish imkonini ancha oshiradi.\n\n"
          "Hozir: <b>" + str(len(rasmlar)) + " / " + str(PORTFOLIO_MAX) + "</b> ta rasm",
          kb=tugmalar([
              [("➕ Rasm qo'shish", "pf_qosh")],
              [("👀 Ko'rish", "pf_" + str(uid))],
              [("🗑 Hammasini o'chirish", "pf_toza")],
          ]))


def portfolio_qosh_boshla(uid):
    if len(profil(uid).get("portfolio", [])) >= PORTFOLIO_MAX:
        yubor(uid, "Portfolio to'la (" + str(PORTFOLIO_MAX) + " ta). Avval tozalang.")
        return
    holat(uid, "portfolio")
    saqla()
    yubor(uid, "📸 Ishlaringiz rasmlarini yuboring (bittadan yoki bir nechtasini).\n"
               "Tugatgach /tayyor yozing.")


def portfolio_rasm(uid, file_id, izoh=""):
    p = profil(uid)
    rasmlar = p.setdefault("portfolio", [])
    if len(rasmlar) >= PORTFOLIO_MAX:
        holat_tozala(uid)
        saqla()
        yubor(uid, "Portfolio to'ldi (" + str(PORTFOLIO_MAX) + " ta). Rahmat!")
        return
    rasmlar.append({"rasm": file_id, "izoh": esc(izoh)[:200], "vaqt": vaqt()})
    saqla()
    yubor(uid, "✅ Qo'shildi (" + str(len(rasmlar)) + "/" + str(PORTFOLIO_MAX)
          + "). Yana yuboring yoki /tayyor")


def portfolio_korsat(kimga, usta_uid):
    p = DATA["foydalanuvchilar"].get(str(usta_uid), {})
    rasmlar = p.get("portfolio", [])
    if not rasmlar:
        yubor(kimga, "Bu hunarmand hali portfolio joylamagan.")
        return
    media = []
    for i, r in enumerate(rasmlar[:PORTFOLIO_MAX]):
        m = {"type": "photo", "media": r["rasm"]}
        if i == 0:
            m["caption"] = ("🖼 " + (p.get("ism") or "Hunarmand") + " ishlari\n"
                            + reyting_matni(usta_uid))
            m["parse_mode"] = "HTML"
        media.append(m)
    if len(media) == 1:
        rasm_yubor(kimga, media[0]["media"], media[0].get("caption", ""))
    else:
        api("sendMediaGroup", chat_id=kimga, media=media)


# =====================  DAM OLISH / TAHRIRLASH  =====================

def pauza_almashtir(uid):
    p = profil(uid)
    p["pauza"] = not p.get("pauza")
    saqla()
    if p["pauza"]:
        yubor(uid, "⏸ <b>Dam olish rejimi yoqildi.</b>\n\n"
                   "Yangi buyurtmalar sizga kelmaydi. Boshlagan ishlaringiz davom etadi.\n"
                   "Qaytish uchun yana «⏸ Dam olish» tugmasini bosing.")
    else:
        yubor(uid, "▶️ <b>Ishga qaytdingiz!</b> Yangi buyurtmalar yana kelib turadi.")


def tahrir_menyu(uid):
    yubor(uid, "✏️ Nimani o'zgartiramiz?", kb=tugmalar([
        [("👤 Ism", "ut_ism"), ("📍 Shahar", "ut_shahar")],
        [("🪡 Ixtisos", "ut_ixtisos"), ("⏳ Tajriba", "ut_tajriba")],
        [("📞 Telefon", "ut_tel")],
    ]))


TAHRIR_SAVOL = {
    "ism": "👤 Yangi ism-familiya:",
    "shahar": "📍 Yangi shahar/tuman:",
    "ixtisos": "🪡 Nima tikasiz?",
    "tajriba": "⏳ Necha yil tajribangiz bor?",
    "tel": "📞 Yangi telefon raqam:",
}


def tahrir_boshla(uid, kalit):
    if kalit not in TAHRIR_SAVOL:
        return
    holat(uid, "usta_tahrir", tahrir_kalit=kalit)
    saqla()
    yubor(uid, TAHRIR_SAVOL[kalit] + "\n<i>Bekor qilish: /bekor</i>")


def tahrir_qabul(uid, matn):
    kalit = holat_ol(uid).get("tahrir_kalit")
    if kalit:
        profil(uid)[kalit] = matn.strip()[:200]
    holat_tozala(uid)
    saqla()
    yubor(uid, "✅ Saqlandi.")


# =====================  MIJOZ ↔ USTA YOZISHUV  =====================

def yozish_boshla(uid, raqam):
    b = DATA["buyurtmalar"].get(raqam)
    if not b or b.get("holat") not in FAOL_HOLATLAR:
        yubor(uid, "Bu buyurtma bo'yicha yozishib bo'lmaydi (yopilgan).")
        return
    if str(uid) not in (str(b.get("mijoz")), str(b.get("usta"))):
        return
    kimga = "hunarmandga" if str(uid) == str(b["mijoz"]) else "mijozga"
    holat(uid, "yoz", yoz_raqam=raqam)
    saqla()
    yubor(uid, "✉️ #" + raqam + " bo'yicha " + kimga + " xabaringizni yozing "
               "(matn yoki rasm).\n<i>Bekor qilish: /bekor</i>")


def yozish_yubor(uid, msg):
    raqam = holat_ol(uid).get("yoz_raqam")
    b = DATA["buyurtmalar"].get(raqam)
    holat_tozala(uid)
    saqla()
    if not b or b.get("holat") not in FAOL_HOLATLAR:
        yubor(uid, "Buyurtma yopilgan, xabar yuborilmadi.")
        return
    mijozmi = str(uid) == str(b["mijoz"])
    qabul = b["usta"] if mijozmi else b["mijoz"]
    kimdan = "👤 Mijozdan" if mijozmi else "🪡 Hunarmanddan"
    sarlavha = "✉️ <b>" + kimdan + " xabar</b> (#" + raqam + ")"
    kb = tugmalar([[("↩️ Javob yozish", "yoz_" + raqam)]])

    if "photo" in msg:
        rasm_yubor(qabul, msg["photo"][-1]["file_id"],
                   sarlavha + ("\n\n" + esc(msg.get("caption", "")) if msg.get("caption") else ""),
                   kb)
    else:
        yubor(qabul, sarlavha + "\n\n" + esc(msg.get("text", "")), kb=kb)

    b.setdefault("yozishuv", []).append({
        "kim": "mijoz" if mijozmi else "usta", "vaqt": vaqt(),
        "matn": esc(msg.get("text") or msg.get("caption") or "[rasm]")[:500]})
    saqla()
    yubor(uid, "✅ Yuborildi.")


# =====================  TAYYOR — RASM BILAN  =====================

def tayyor_boshla(uid, raqam):
    b = DATA["buyurtmalar"].get(raqam)
    if not b or str(b.get("usta")) != str(uid):
        return
    if b.get("holat") != "tikilmoqda":
        yubor(uid, "Bu buyurtma hozir «tikilmoqda» holatida emas "
                   "(to'lov tasdiqlanmagan yoki allaqachon topshirilgan).")
        return
    holat(uid, "tayyor_rasm", tayyor_raqam=raqam)
    saqla()
    yubor(uid, "📸 Tayyor kiyimning rasmini yuboring — mijoz ko'rib xursand bo'ladi.\n"
               "Rasm bo'lmasa /otkaz yozing.")
