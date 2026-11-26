"""Texnik topshiriq 10-bo'lim: test mezonlari."""
import re
from yordamchi import *  # noqa
import suhbat, zaxira, json

U = 222
for u in (U, 101, 102, 103, 104): msg(u, "/start"); cb(u, "til_uz")
msg(U, "🪡 Men hunarmandman")
for x in ["Zulfiya", "Nukus", "ko'ylak", "10", "+998901112233"]: msg(U, x)
cb(A, "utasdiq_222")

M = 101
msg(M, "🤖 AI bilan buyurtma"); msg(M, "Rang-barang adras qo'l sumka kerak")
for x in ["O'rtacha", "to'rtburchak", "Ikkalasi ham", "Ikkita", "Fermuar", "munchoq"]: msg(M, x)
k = D["holatlar"][str(M)]["karta"]
ok(k["tur"] == "sumka", "Sumka turi aniqlandi")
qs = [x[2] for x in LOG if x[1] == M and x[2].startswith("❓")]
ok(len(qs) == len(set(qs)), "Savollar takrorlanmadi")
cb(M, "v_ok"); msg(M, "2 hafta"); msg(M, "+998901234567")
ok(not re.search(r"Bo'yingiz|Yengi|Ko'krak", matnlar(M)), "Sumkada bo'y/yeng/ko'krak so'ralmadi")
ok("Yakuniy buyurtma kartasi" in oxirgi(M)[2] and not D["buyurtmalar"], "Tasdiqdan oldin karta, buyurtma yuborilmagan")
cb(M, "v_yubor"); ok(len(D["buyurtmalar"]) == 1, "Tasdiqdan keyin yuborildi")

M = 102
msg(M, "🤖 AI bilan buyurtma"); msg(M, "To'yga ko'k adras zamonaviy ko'ylak kerak")
for x in ["uzun", "uzun yeng", "tik yoqa"]: msg(M, x)
cb(M, "v_ok"); ok("Bo'yingiz" in matnlar(M), "Ko'ylakda bo'y so'raldi")

M = 103
msg(M, "🤖 AI bilan buyurtma"); msg(M, "Qizil atlas ko'ylak kerak"); msg(M, "Ko'ylak emas, sumka")
k = D["holatlar"][str(M)]["karta"]
ok(k["tur"] == "sumka" and k["maydonlar"].get("rang") == "qizil", "«Ko'ylak emas, sumka»")
msg(M, "boshqa rang"); ok("rang" not in k["maydonlar"], "«Boshqa rang»")
msg(M, "buyurtmani bekor qil"); ok(any(c == "v_bekor" for _, c in oxirgi(M)[3]), "Bekor qilishdan oldin tasdiq")

r = "1001"; cb(U, "n_" + r); msg(U, "300000"); msg(U, "7"); msg(U, "-")
cb(999, "tanla_1001_222"); ok(D["buyurtmalar"][r]["holat"] == "yangi", "Begona tasdiqlay olmaydi")
cb(101, "tanla_1001_222"); ok("Tasdiqlandi" in bot.holat_nomi(D["buyurtmalar"][r]), "Vakolatli tomon tasdiqladi")

# Zaxira va tiklash
yub = {}
zaxira._hujjat_yubor = lambda c, n, m, i="": yub.update(m=m) or {"result": {"document": {"file_id": "X"}}}
msg(A, "💾 Zaxira"); ok(json.loads(yub["m"])["buyurtmalar"].get("1001"), "Zaxira fayli to'liq")
msg(999, "/tiklash"); ok(D["holatlar"].get("999", {}).get("bosqich") != "tiklash", "Begona tiklay olmaydi")
for b in ["👗 Dizaynlar", "🛍 Do'kon", "🛒 Savatim", "📦 Buyurtmalarim", "🌐 Til", "📚 Kataloglar", "ℹ️ Yordam"]:
    n = len(LOG); msg(104, b); ok(len(LOG) > n, "Tugma: " + b)
ok(not any("🏳" in str(x) for x in LOG), "Oq bayroq yo'q")
