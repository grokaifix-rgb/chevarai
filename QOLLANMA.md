# 🧵 Chevar AI — qo'llanma

Botda **uch bo'lim** bor:

| Bo'lim | Kim uchun | Nima bo'ladi |
|---|---|---|
| 🤖 **AI bilan buyurtma** | Aniq xohishi bor mijoz | O'z so'zi bilan aytadi → bot aniq varaqa qiladi → hunarmandlar narx beradi |
| 👗 **Dizaynlar** | "Ko'rsatsangiz tanlayman" deydigan mijoz | Tayyor namunalardan tanlaydi → faqat o'lchamini beradi |
| 🛍 **Do'kon** | Tez olmoqchi mijoz | O'lchami tayyor mahsulot → savat → to'lov → uyigacha yetkazish |

---

## 1. Botni ishga tushirish

### Uy kompyuterida
1. `SOZLASH.command` — token, admin ID lar, karta, komissiya, yetkazish narxi
2. `ISHGA-TUSHIRISH.command` — botni yoqadi
3. `AVTOMATIK-YOQISH.command` — kompyuter yonganda o'zi ishga tushadi
4. `TOXTATISH.command` — to'xtatadi

### Serverda (Railway)
Sozlamalar fayl orqali emas, **Variables** (muhit o'zgaruvchilari) orqali beriladi.
Ro'yxati README.md da.

---

## 2. Mijoz nima ko'radi

Menyu:

```
🤖 AI bilan buyurtma
👗 Dizaynlar        🛍 Do'kon
🛒 Savatim          📦 Buyurtmalarim
ℹ️ Yordam           🪡 Men hunarmandman
```

### 🤖 AI bilan buyurtma
Mijoz yozadi: *«To'yga ko'k adras matodan zamonaviy ko'ylak kerak»*
→ bot yetishmagan narsani so'raydi → **buyurtma varaqasi** → o'lchamlar
(bo'y, ko'krak, bel, son) → muddat → telefon → buyurtma hunarmandlarga tarqaladi.

### 👗 Dizaynlar
Rasm bilan namunalar chiqadi. «Shu dizaynda buyurtma berish» → faqat o'lcham
va muddat so'raladi. Qolgani AI buyurtmasi bilan bir xil: hunarmandlar narx beradi.

### 🛍 Do'kon
Kategoriya → mahsulot (rasm, narx, mavjud o'lchamlar) → o'lcham → savat.
Savatda son o'zgartiriladi. Rasmiylashtirishda:
- 🏠 **Yetkazib berish** — manzil so'raladi, narxi qo'shiladi
- 🏪 **O'zim olib ketaman** — yetkazish bepul

Belgilangan summadan katta xaridda yetkazish **bepul**.
To'lov: karta → chek rasmi → admin tasdiqlaydi → 🚚 yo'lga chiqdi → ✅ topshirildi.

---

## 3. Hunarmand nima qiladi

1. «🪡 Men hunarmandman» → 5 savol (ism, shahar, ixtisos, tajriba, telefon)
2. Admin tasdiqlaydi
3. Yangi buyurtmalar avtomatik keladi (dizayn tanlangan bo'lsa — rasmi bilan)
4. «💰 Narx taklif qilish» → o'z narxi + necha kun
5. Mijoz tanlasa xabar keladi → to'lovdan keyin ishni boshlaydi
6. «✅ Tayyor bo'ldi» → mijoz qolgan to'lovni qiladi → hunarmand baholanadi

---

## 4. Admin nima qiladi

`/admin` buyrug'i. **Bir nechta admin** bo'lishi mumkin — hammasiga bir xil
xabar boradi.

Panel tugmalari:
- 🪡 **Hunarmand arizalari** — tasdiqlash / rad etish
- 🤖 **Tikish buyurtmalari** — faol buyurtmalar ro'yxati
- 🛍 **Do'kon buyurtmalari** — to'lovni tasdiqlash, 🚚 yo'lga chiqdi, ✅ topshirildi
- 👗 **Dizayn qo'shish** — nom, tavsif, mato, rang, narx, **rasm**
- 🛒 **Mahsulot qo'shish** — nom, tavsif, kategoriya, narx, o'lchamlar (`S:2, M:5, L:3`), **rasm**
- 📋 **Ro'yxat** — qo'shilganlarni ko'rish

Yashirish/qayta yoqish: `/ochir D3` yoki `/ochir M5`

Statistikada: foydalanuvchilar, hunarmandlar, tikish aylanmasi va **foydasi**,
do'kon aylanmasi.

---

## 5. Pul qanday hisoblanadi

**Tikish buyurtmalarida** hunarmand o'z narxini yozadi, bot ustiga komissiyani qo'shadi.

Komissiya 30% da:

| Kim | Qancha |
|---|---|
| Hunarmand yozgan narx | 500 000 so'm |
| Mijozga ko'rinadigan narx | **715 000 so'm** |
| Sizga qoladi | **215 000 so'm** |
| Oldindan to'lov (50%) | 358 000 so'm |

**Do'konda** narxni siz to'g'ridan-to'g'ri belgilaysiz — foyda to'liq sizniki
(tan narxidan tashqari).

Yetkazib berish narxi va bepul chegarasi sozlamada.

---

## 6. AI haqida

**A) Kalitsiz** — ichki lug'at mato, rang, fason, kiyim turi va tadbirni matndan
o'zi topadi. Tekin, internetsiz ham ishlaydi.

**B) Kalit bilan** (hozir ulangan: **Google Gemini**, bepul) — jonli suhbat,
maslahat beradi, aniqroq savol qo'yadi.
Kalit: https://aistudio.google.com/apikey

AI ishlamay qolsa (kalit tugadi, internet yo'q) bot **avtomat** kalitsiz rejimga
o'tadi va to'xtamaydi.

---

## 7. Maxfiylik

`config.json` (token, karta, AI kalit) va `data.json` (mijozlar bazasi)
GitHubga **tushmaydi** — `.gitignore` da. Serverda bu ma'lumotlar Variables
ichida saqlanadi.

`data.json` — butun bazangiz. Vaqti-vaqti bilan nusxasini saqlang.

---

## 8. Tez-tez uchraydigan savollar

**Buyurtma hunarmandlarga bormadi?**
Tasdiqlangan hunarmand yo'q. `/admin` → «Hunarmand arizalari».

**Do'konda mahsulot ko'rinmayapti?**
Zaxirasi tugagan yoki `/ochir` bilan yashirilgan bo'lishi mumkin.

**Rasm qo'shilmadi?**
Rasmni **rasm** sifatida yuboring (fayl sifatida emas).

**Bot javob bermayapti?**
Railway'da: Deployments → Logs. Uyda: `bot.log` fayli.

---

## 9. Keyingi bosqichlar

- [ ] Hunarmandlar reytingi bo'yicha saralash va portfolio
- [ ] Rus va ingliz tillari (chet el mijozlari)
- [ ] Click/Payme orqali avtomatik to'lov
- [ ] Kuryer holatini kuzatish (trek raqami)
- [ ] Chegirmalar va promo-kodlar

---

Muallif: **Mirzabek Shukurullayev** · 📞 +998910964410 · Telegram: @diumuser
