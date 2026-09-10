# 🧵 Chevar AI

O'zbek hunarmandchiligini raqamlashtiruvchi Telegram platformasi.
Mijoz oddiy tilda yozadi — AI uni hunarmand tushunadigan aniq buyurtmaga aylantiradi.

## Uch bo'lim

| Bo'lim | Nima qiladi |
|---|---|
| 🤖 **AI bo'limi** | Mijoz o'z so'zi bilan yozadi, bot savol berib aniq buyurtma varaqasini tayyorlaydi va hunarmandlarga uzatadi. Ular narx taklif qiladi, mijoz tanlaydi. |
| 👗 **Dizaynlar** | Tayyor namunalar katalogi. Mijoz yoqqanini tanlaydi, faqat o'lchamini beradi — o'ziga moslab tikiladi. |
| 🛍 **Do'kon** | O'lchami aniq tayyor mahsulotlar (S/M/L/XL). Savat, yetkazib berish, to'lov. |

## Pul mantiqi

Hunarmand o'z narxini (mato + mehnat) yozadi, platforma ustiga komissiya qo'shadi:

```
umumiy = usta_narxi / (1 - komissiya/100)
```

Komissiya 30% da: usta **500 000** → mijoz **715 000** → platforma **215 000**.
Do'kon savdosida narx to'g'ridan-to'g'ri belgilanadi.

Yetkazib berish: belgilangan summadan yuqori xaridda bepul.

## Texnik tomoni

- Sof Python 3, tashqi kutubxona **kerak emas** (faqat standart kutubxona)
- Telegram Bot API — long polling
- Ma'lumotlar `data.json` faylida (Railway'da Volume ichida)
- AI: Google Gemini / Claude / OpenAI-mos. **Kalitsiz ham ishlaydi** — ichki
  kalit so'zlar tahlili bilan. AI uzilsa avtomat shu rejimga tushadi.

### Fayllar

| Fayl | Vazifasi |
|---|---|
| `bot.py` | Asosiy sikl, AI buyurtma oqimi, hunarmand qismi, marshrutlash |
| `core.py` | Sozlamalar (env + config.json), ma'lumotlar, Telegram API |
| `dokon.py` | Dizaynlar, do'kon, savat, yetkazib berish |
| `admin.py` | Admin panel, kontent qo'shish, buyurtmalarni boshqarish |
| `ai.py` | Buyurtmani tushunish (AI + offline tahlil) |
| `sozlash.py` | Uy kompyuterida savol-javob orqali sozlash |

## Ishga tushirish

### Uy kompyuterida (macOS)

```bash
python3 sozlash.py   # yoki SOZLASH.command
python3 bot.py       # yoki ISHGA-TUSHIRISH.command
```

`AVTOMATIK-YOQISH.command` — kompyuter yonganda bot o'zi ishga tushadi.

### Serverda (Railway)

`Procfile` → `worker: python bot.py`

Muhit o'zgaruvchilari (Variables):

| O'zgaruvchi | Misol |
|---|---|
| `BOT_TOKEN` | BotFather tokeni |
| `ADMIN_IDS` | `5939503983,8780230235` |
| `DATA_DIR` | `/data` (Volume ulanadi) |
| `AI_PROVIDER` | `gemini` |
| `AI_KEY` | Google AI Studio kaliti |
| `CARD_NUMBER` / `CARD_OWNER` | To'lov kartasi |
| `KOMISSIYA_FOIZ` | `30` |
| `YETKAZISH_NARX` | `25000` |
| `BEPUL_YETKAZISH` | `500000` |

⚠️ `config.json` va `data.json` GitHubga tushmaydi (`.gitignore`). Serverda
sozlamalar faqat muhit o'zgaruvchilaridan o'qiladi.

## Batafsil qo'llanma

O'zbek tilidagi to'liq qo'llanma: [QOLLANMA.md](QOLLANMA.md)

---

Muallif: **Mirzabek Shukurullayev** · 📞 +998910964410 · Telegram: [@diumuser](https://t.me/diumuser)
