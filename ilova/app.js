/* Chevar AI — Telegram Mini App. Muallif: Mirzabek Shukurullayev · @diumuser */
"use strict";
const tg = window.Telegram ? window.Telegram.WebApp : null;
const H = { men: null, token: "", turlar: null, sahifa: "bosh", tarix: [], savat: 0, kesh: {} };

/* ---------------- tarjima (interfeys matnlari) ---------------- */
const T = {
  "Bosh": ["Bas bet", "Home"], "Dizaynlar": ["Dizaynlar", "Designs"], "Do'kon": ["Dúkan", "Shop"],
  "Buyurtmalar": ["Buyırtpalar", "Orders"], "Men": ["Men", "Me"],
  "AI bilan buyurtma": ["AI menen buyırtpa", "Order with AI"],
  "Xohishingizni yozing — AI aniq buyurtma kartasini tuzadi, hunarmandlar narx taklif qiladi.":
    ["Qálewińizdi jazıń — AI anıq buyırtpa kartasın dúzedi, sheberler baha usınadı.",
     "Describe what you want — AI builds a precise order card, artisans send offers."],
  "Boshlash": ["Baslaw", "Start"], "Matolar": ["Matalar", "Fabrics"], "O'lchamlar": ["Ólshemler", "Sizes"],
  "Akademiya": ["Akademiya", "Academy"], "Hunarmandlar": ["Sheberler", "Artisans"],
  "Sevimlilar": ["Saylanǵanlar", "Favourites"], "Qidiruv": ["Izlew", "Search"],
  "Qidirish: dizayn, mato, mahsulot, usta...": ["Izlew: dizayn, mata, ónim, sheber...", "Search designs, fabrics, products, artisans..."],
  "Nima kerak?": ["Ne kerek?", "What do you need?"],
  "Masalan: to'yga ko'k adras ko'ylak kerak": ["Mısalı: toyǵa kók adras kóylek kerek", "E.g. a blue ikat dress for a wedding"],
  "AI tahlil qilsin": ["AI talqılasın", "Let AI analyse"], "yoki turini tanlang": ["yamasa túrin saylań", "or choose a type"],
  "Davom etish": ["Dawam etiw", "Continue"], "Orqaga": ["Artqa", "Back"], "Farqi yo'q": ["Parqı joq", "Any"],
  "O'lchamlar va muddat": ["Ólshemler hám múddet", "Sizes and deadline"],
  "Saqlangan o'lchamlarim": ["Saqlanǵan ólshemlerim", "My saved sizes"],
  "O'lchamni maslahat bering": ["Ólshem boyınsha másláhát", "Suggest my size"],
  "Kim uchun?": ["Kim ushın?", "For whom?"], "Ayol": ["Hayal", "Woman"], "Erkak": ["Er adam", "Man"], "Bola": ["Bala", "Child"],
  "Bo'y (sm)": ["Boy (sm)", "Height (cm)"], "Vazn (kg)": ["Salmaq (kg)", "Weight (kg)"],
  "Maslahat olish": ["Másláhát alıw", "Get advice"], "Qachonga kerak?": ["Qashanǵa kerek?", "When do you need it?"],
  "Telefon": ["Telefon", "Phone"], "Buyurtma kartasi": ["Buyırtpa kartası", "Order card"],
  "Tasdiqlayman, yuborilsin": ["Tastıyıqlayman, jiberilsin", "Confirm and send"],
  "Narx va muddatni hunarmand taklif qiladi. AI narx o'ylab topmaydi.":
    ["Baha hám múddetti sheber usınadı. AI baha oylap tappaydı.", "Artisans propose price and deadline. AI never invents prices."],
  "Buyurtma yuborildi!": ["Buyırtpa jiberildi!", "Order sent!"],
  "Shu dizaynda buyurtma": ["Usı dizaynda buyırtpa", "Order this design"],
  "Hammasi": ["Hámmesi", "All"], "O'zbek": ["Ózbek", "Uzbek"], "Qoraqalpoq": ["Qaraqalpaq", "Karakalpak"],
  "Savatga": ["Sebetke", "Add to cart"], "Savat": ["Sebet", "Cart"], "Savat bo'sh": ["Sebet bos", "Cart is empty"],
  "O'lchamni tanlang": ["Ólshemdi saylań", "Choose size"], "Sotuvchi": ["Satıwshı", "Seller"],
  "Mahsulotlar": ["Ónimler", "Products"], "Yetkazish": ["Jetkerip beriw", "Delivery"], "bepul": ["biypul", "free"],
  "Jami": ["Jámi", "Total"], "Rasmiylashtirish": ["Rásmiylestiriw", "Checkout"],
  "Yetkazib berish": ["Jetkerip beriw", "Delivery"], "O'zim olib ketaman": ["Ózim alıp ketemen", "Pick up"],
  "Manzil": ["Mánzil", "Address"], "Tikish": ["Tigiw", "Tailoring"],
  "Hali buyurtma yo'q": ["Ele buyırtpa joq", "No orders yet"], "Takliflar": ["Usınıslar", "Offers"],
  "Tanlash": ["Saylaw", "Choose"], "Savol berish": ["Soraw beriw", "Ask"], "Sharhlar": ["Pikirler", "Reviews"],
  "To'lov": ["Tólem", "Payment"], "Karta": ["Karta", "Card"], "Chek rasmini yuborish": ["Chek súwretin jiberiw", "Upload receipt"],
  "Qabul qilib oldim": ["Qabıl alıp aldım", "I received it"], "Baholang": ["Bahalań", "Rate"],
  "Sharh yozing": ["Pikir jazıń", "Write a review"], "Yuborish": ["Jiberiw", "Send"],
  "Bekor qilish": ["Biykarlaw", "Cancel"], "Hunarmandga yozish": ["Sheberge jazıw", "Message artisan"],
  "Xabar": ["Xabar", "Message"], "Takliflar kutilmoqda": ["Usınıslar kútilmekte", "Waiting for offers"],
  "Ism": ["Atı", "Name"], "Til": ["Til", "Language"], "Saqlash": ["Saqlaw", "Save"],
  "Operatorga yozish": ["Operatorǵa jazıw", "Contact support"],
  "Hunarmand bo'lish": ["Sheber bolıw", "Become an artisan"], "Shahar": ["Qala", "City"],
  "Nima tikasiz?": ["Ne tigesiz?", "What do you sew?"], "Tajriba (yil)": ["Tájiriybe (jıl)", "Experience (years)"],
  "Ariza yuborish": ["Arza jiberiw", "Apply"], "Ariza ko'rib chiqilmoqda": ["Arza kórip shıǵılmaqta", "Application under review"],
  "Hunarmand paneli": ["Sheber paneli", "Artisan panel"], "Yangi buyurtmalar": ["Jańa buyırtpalar", "New orders"],
  "Mening ishlarim": ["Meniń jumıslarım", "My jobs"], "Narx taklif qilish": ["Baha usınıw", "Send offer"],
  "Narx (mato + mehnat), so'm": ["Baha (mata + miynet), swm", "Price (fabric + labour), UZS"],
  "Necha kun": ["Neshe kún", "Days"], "Izoh": ["Túsindirme", "Note"], "Rad etish": ["Biykarlaw", "Decline"],
  "Tayyor bo'ldi": ["Tayar boldı", "Ready"], "Dam olish": ["Dem alıw", "Take a break"], "Portfolio": ["Portfolio", "Portfolio"],
  "Rasm qo'shish": ["Súwret qosıw", "Add photo"], "Ishlab topilgan": ["Tabıs", "Earned"],
  "Admin paneli": ["Admin paneli", "Admin panel"], "To'lovlar": ["Tólemler", "Payments"],
  "Tasdiqlash": ["Tastıyıqlaw", "Approve"], "Rad": ["Biykar", "Reject"], "Foydalanuvchilar": ["Paydalanıwshılar", "Users"],
  "Bloklash": ["Bloklaw", "Block"], "Qo'shish": ["Qosıw", "Add"], "Zaxira olish": ["Zaxira alıw", "Backup"],
  "Mahsulot qo'shish": ["Ónim qosıw", "Add product"], "Dizayn qo'shish": ["Dizayn qosıw", "Add design"],
  "Dars qo'shish": ["Sabaq qosıw", "Add lesson"], "Shu matodan buyurtma": ["Usı matadan buyırtpa", "Order with this fabric"],
  "Mos kiyimlar": ["Sáykes kiyimler", "Good for"], "Parvarish": ["Kútim", "Care"], "Tarkibi": ["Quramı", "Composition"],
  "Darslar tez orada": ["Sabaqlar tez arada", "Lessons coming soon"], "YouTube'da ko'rish": ["YouTube'ta kóriw", "Watch on YouTube"],
  "Telegramga yuborish": ["Telegramǵa jiberiw", "Send to Telegram"], "Ochish": ["Ashıw", "Open"],
  "Topilmadi": ["Tabılmadı", "Nothing found"], "Saqlandi": ["Saqlandı", "Saved"], "Xato": ["Qáte", "Error"],
  "Muddat": ["Múddet", "Deadline"], "Usta": ["Sheber", "Artisan"], "Hunarmand": ["Sheber", "Artisan"],
  "Bajarilgan ishlar": ["Orınlanǵan jumıslar", "Completed jobs"], "baho": ["baha", "ratings"],
  "Telegramga yubordik": ["Telegramǵa jiberdik", "Sent to Telegram"], "Kategoriya": ["Kategoriya", "Category"],
  "Narx": ["Baha", "Price"], "Tavsif": ["Táriyp", "Description"], "Nomi": ["Atı", "Name"], "Rasm": ["Súwret", "Photo"],
  "Statistika": ["Statistika", "Statistics"], "Topshirildi": ["Tapsırıldı", "Delivered"], "Yo'lga chiqdi": ["Jolǵa shıqtı", "Shipped"],
};
const TIL_I = { kaa: 0, kaa_cyr: 0, en: 1 };

/* lotin → kirill (bot bilan bir xil qoidalar) */
const KIR = (() => {
  const UZ = { a: "а", b: "б", d: "д", e: "е", f: "ф", g: "г", h: "ҳ", i: "и", j: "ж", k: "к", l: "л", m: "м", n: "н",
    o: "о", p: "п", q: "қ", r: "р", s: "с", t: "т", u: "у", v: "в", x: "х", y: "й", z: "з" };
  const KAA = Object.assign({}, UZ, { w: "ў", á: "ә", ó: "ө", ú: "ү", ı: "ы", ń: "ң", ǵ: "ғ" });
  const TUT = "'’‘ʻʼ`";
  function bolak(s, xarita, uzmi) {
    let r = "";
    for (let i = 0; i < s.length; i++) {
      const c = s[i], l = c.toLowerCase(), j = s.slice(i, i + 2).toLowerCase(), katta = c !== l;
      let k = null, n = 1;
      if (uzmi && (l === "o" || l === "g") && TUT.includes(s[i + 1] || "")) { k = l === "o" ? "ў" : "ғ"; n = 2; }
      else if (j === "sh") { k = "ш"; n = 2; } else if (j === "ch") { k = "ч"; n = 2; }
      else if (j === "yo" && !TUT.includes(s[i + 2] || "")) { k = "ё"; n = 2; }
      else if (j === "yu") { k = "ю"; n = 2; } else if (j === "ya") { k = "я"; n = 2; }
      else if (j === "ye") { k = "е"; n = 2; }
      else if (l === "e") { const o = s[i - 1] || " "; k = /[a-zа-яәөүы]/i.test(o) && !/[aeiouáóúı]/i.test(o) ? "е" : "э"; }
      else if (TUT.includes(c) && /\w/.test(s[i - 1] || "") && /\w/.test(s[i + 1] || "")) k = "ъ";
      else if (xarita[l]) k = xarita[l];
      if (k === null) { r += c; continue; }
      r += katta ? (n === 2 && s[i + 1] && s[i + 1] === s[i + 1].toLowerCase() ? k[0].toUpperCase() + k.slice(1) : k.toUpperCase()) : k;
      i += n - 1;
    }
    return r;
  }
  const HIMOYA = /(<[^>]+>|https?:\/\/\S+|@\w+|\bAI\b|\bUZS\b)/;
  return (s, kaa) => String(s).split(HIMOYA).map(q => HIMOYA.test(q) ? q : bolak(q, kaa ? KAA : UZ, !kaa)).join("");
})();

function t(s) {
  const til = (H.men && H.men.til) || "uz";
  let r = s;
  if (til in TIL_I && T[s]) r = T[s][TIL_I[til]];
  if (til === "uz_cyr") r = KIR(r, false);
  if (til === "kaa_cyr") r = KIR(r, true);
  return r;
}
function tc(s) { /* serverdan kelgan o'zbekcha matnni faqat kirillga o'giradi */
  const til = (H.men && H.men.til) || "uz";
  return til === "uz_cyr" ? KIR(s, false) : til === "kaa_cyr" ? KIR(s, true) : s;
}

/* ---------------- yordamchilar ---------------- */
const $ = (s, el = document) => el.querySelector(s);
const un = s => String(s == null ? "" : s).replace(/&(amp|lt|gt|quot|#39);/g, (_, k) => ({ amp: "&", lt: "<", gt: ">", quot: '"', "#39": "'" }[k]));
const e = s => un(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const pul = n => (Math.round(+n || 0)).toLocaleString("ru-RU").replace(/,/g, " ") + " " + (((H.men || {}).til || "").startsWith("en") ? "UZS" : "so'm");
const ON = { razmer: "O'lcham", boy: "Bo'y", kokrak: "Ko'krak", bel: "Bel", son: "Son" };
const oN = k => tc(ON[k] || k);
const titra = (k = "light") => { try { tg && tg.HapticFeedback.impactOccurred(k); } catch (_) {} };

function bildir(matn, xato) {
  const d = document.createElement("div");
  d.className = "bildirish" + (xato ? " xato" : "");
  d.textContent = matn;
  document.body.appendChild(d);
  setTimeout(() => d.remove(), 2800);
  if (xato) { try { tg && tg.HapticFeedback.notificationOccurred("error"); } catch (_) {} }
}

async function api(yol, d = {}) {
  const r = await fetch("/api/" + yol, { method: "POST", headers: { "Content-Type": "application/json", "X-Token": H.token },
    body: JSON.stringify(d) });
  let j = {};
  try { j = await r.json(); } catch (_) {}
  if (!r.ok) { const x = new Error(j.xato || ("Xato " + r.status)); x.kod = r.status; throw x; }
  return j;
}
async function urin(fn) {
  try { return await fn(); } catch (x) { bildir(tc(x.message), true); throw x; }
}

/* rasmni kichraytirib base64 qiladi (telefon rasmlari katta bo'ladi) */
function rasmTanla() {
  return new Promise((ok) => {
    const inp = document.createElement("input");
    inp.type = "file"; inp.accept = "image/*";
    inp.onchange = () => {
      const f = inp.files[0]; if (!f) return ok(null);
      const img = new Image();
      img.onload = () => {
        const m = Math.min(1, 1600 / Math.max(img.width, img.height));
        const c = document.createElement("canvas");
        c.width = img.width * m; c.height = img.height * m;
        c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
        ok(c.toDataURL("image/jpeg", 0.85));
      };
      img.src = URL.createObjectURL(f);
    };
    inp.click();
  });
}

/* ---------------- navigatsiya ---------------- */
const TABLAR = [["bosh", "🏠", "Bosh"], ["dizaynlar", "👗", "Dizaynlar"], ["dokon", "🛍", "Do'kon"],
  ["buyurtmalar", "📦", "Buyurtmalar"], ["men", "👤", "Men"]];

function nav() {
  const n = $("#nav");
  n.hidden = false;
  n.innerHTML = TABLAR.map(([k, ic, nom]) => `<button data-t="${k}" class="${H.asos === k ? "tan" : ""}"><span>${ic}</span>${e(t(nom))}
    ${k === "dokon" && H.savat ? `<i class="nishon">${H.savat}</i>` : ""}</button>`).join("");
  n.querySelectorAll("button").forEach(b => b.onclick = () => { titra(); H.tarix = []; och(b.dataset.t); });
}

function och(sahifa, param, tarixga) {
  if (tarixga) H.tarix.push([H.sahifa, H.param]);
  H.sahifa = sahifa; H.param = param;
  if (TABLAR.some(x => x[0] === sahifa)) H.asos = sahifa;
  nav();
  window.scrollTo(0, 0);
  const bb = tg && tg.BackButton;
  if (bb) { H.tarix.length ? bb.show() : bb.hide(); }
  const el = $("#ilova");
  el.innerHTML = `<div class="yuklanmoqda"><div class="igna"></div></div>`;
  (SAHIFALAR[sahifa] || SAHIFALAR.bosh)(el, param).catch(x => {
    el.innerHTML = `<div class="bosh-holat"><span>⚠️</span>${e(tc(x.message))}</div>`;
  });
}
function orqaga() {
  const o = H.tarix.pop();
  if (o) { och(o[0], o[1]); } else och("bosh");
}
function ichkiSarlavha(nom) {
  return `<header class="ichki"><button class="orqa" onclick="orqaga()">‹</button><h2>${e(nom)}</h2></header>`;
}

function varaq(html) {
  const v = document.createElement("div");
  v.className = "varaq";
  v.innerHTML = `<div class="ich"><div class="tutqich"></div>${html}</div>`;
  v.onclick = ev => { if (ev.target === v) v.remove(); };
  document.body.appendChild(v);
  return v;
}

const SAHIFALAR = {};

/* ---------------- Bosh sahifa ---------------- */
SAHIFALAR.bosh = async (el) => {
  const m = H.men;
  el.innerHTML = `
  <header class="bosh"><h1>Chevar AI</h1><p>${e(t("Assalomu alaykum"))}${m.ism ? ", " + e(m.ism) : ""}!</p></header>
  <div class="tasma"></div>
  <main>
    <div class="ai-karta" id="aiK"><h2>🤖 ${e(t("AI bilan buyurtma"))}</h2>
      <p>${e(t("Xohishingizni yozing — AI aniq buyurtma kartasini tuzadi, hunarmandlar narx taklif qiladi."))}</p>
      <button class="tugma tilla" style="width:auto">${e(t("Boshlash"))} →</button><div class="tasma"></div></div>
    <input id="qid" placeholder="🔍 ${e(t("Qidirish: dizayn, mato, mahsulot, usta..."))}">
    <div class="tez">
      <button data-o="dizaynlar"><span>👗</span>${e(t("Dizaynlar"))}</button>
      <button data-o="dokon"><span>🛍</span>${e(t("Do'kon"))}</button>
      <button data-o="matolar"><span>🧵</span>${e(t("Matolar"))}</button>
      <button data-o="olchamlar"><span>📐</span>${e(t("O'lchamlar"))}</button>
      <button data-o="akademiya"><span>🎓</span>${e(t("Akademiya"))}</button>
      <button data-o="ustalar"><span>🪡</span>${e(t("Hunarmandlar"))}</button>
    </div>
    <div class="bolim-nom">✨ ${e(t("Dizaynlar"))}</div>
    <div class="siljish" id="yangiDz"><div class="xira">…</div></div>
  </main>`;
  $("#aiK").onclick = () => { titra(); och("ai", null, true); };
  el.querySelectorAll(".tez button").forEach(b => b.onclick = () => { titra(); och(b.dataset.o, null, true); });
  $("#qid").onkeydown = ev => { if (ev.key === "Enter" && ev.target.value.trim()) och("qidiruv", ev.target.value.trim(), true); };
  const dz = await dizaynlarOl();
  $("#yangiDz").innerHTML = dz.slice(-8).reverse().map(d => `
    <div class="tovar" style="width:130px;flex:none" data-id="${e(d.id)}"><div class="r" style="background-image:url('${d.rasm}')"></div>
    <div class="i"><b>${e(tc(d.nom))}</b></div></div>`).join("");
  $("#yangiDz").querySelectorAll(".tovar").forEach(x => x.onclick = () => dizaynVaraq(dz.find(d => d.id === x.dataset.id)));
};
T["Assalomu alaykum"] = ["Assalawma áleykum", "Welcome"];

/* ---------------- AI buyurtma (bosqichli shakl) ---------------- */
async function turlarOl() {
  if (!H.turlar) H.turlar = await api("turlar");
  return H.turlar;
}

SAHIFALAR.ai = async (el, p) => {
  const tl = await turlarOl();
  const b = H.buyurtma = p && p.karta ? Object.assign({ olcham: {}, muddat: "", tel: H.men.tel || "" }, p)
    : { karta: { tur: null, maydonlar: {}, izoh: "" }, olcham: {}, muddat: "", tel: H.men.tel || "", dizayn: "" };
  b.karta.maydonlar = b.karta.maydonlar || {};
  aiQadam1(el, tl, b);
};

function aiQadam1(el, tl, b) {
  el.innerHTML = ichkiSarlavha(t("AI bilan buyurtma")) + `<main>
    <div class="karta"><h3>${e(t("Nima kerak?"))}</h3>
      <textarea id="aiMatn" placeholder="${e(t("Masalan: to'yga ko'k adras ko'ylak kerak"))}"></textarea>
      <button class="tugma" id="aiBos" style="margin-top:10px">🤖 ${e(t("AI tahlil qilsin"))}</button>
      <p class="xira" style="margin:14px 0 8px">${e(t("yoki turini tanlang"))}:</p>
      <div class="chiplar">${Object.entries(tl.turlar).map(([k, v]) =>
        `<button class="chip ${b.karta.tur === k ? "tan" : ""}" data-k="${e(k)}">${e(tc(v.nom))}</button>`).join("")}</div>
    </div></main>`;
  el.querySelectorAll(".chip").forEach(c => c.onclick = () => {
    titra(); b.karta.tur = c.dataset.k; aiQadam2(el, tl, b);
  });
  $("#aiBos").onclick = async () => {
    const matn = $("#aiMatn").value.trim();
    if (!matn) return bildir(t("Nima kerak?"), true);
    const btn = $("#aiBos"); btn.disabled = true; btn.textContent = "🤖 …";
    try {
      const r = await urin(() => api("ai_ajrat", { matn, karta: b.karta }));
      b.karta = r.karta;
      if (!b.karta.tur) { bildir(t("yoki turini tanlang"), true); btn.disabled = false; btn.textContent = "🤖 " + t("AI tahlil qilsin"); return; }
      aiQadam2(el, tl, b);
    } catch (_) { btn.disabled = false; btn.textContent = "🤖 " + t("AI tahlil qilsin"); }
  };
}

function aiQadam2(el, tl, b) {
  const tur = tl.turlar[b.karta.tur];
  const my = b.karta.maydonlar;
  el.innerHTML = ichkiSarlavha(tc(tur.nom)) + `<main><div class="karta">
    ${tur.maydonlar.map(f => {
      const v = tl.variantlar[f.kalit] || [];
      return `<label>${e(tc(f.savol))}</label>
        <input data-k="${e(f.kalit)}" value="${e(my[f.kalit] || "")}">
        <div class="siljish" style="margin-top:6px">${v.map(x => `<button class="chip" data-k="${e(f.kalit)}" data-v="${e(x)}">${e(tc(x))}</button>`).join("")}
        <button class="chip farq" data-k="${e(f.kalit)}" data-v="farqi yo'q">${e(t("Farqi yo'q"))}</button></div>`;
    }).join("")}
    <label>${e(t("Izoh"))}</label><textarea id="izoh">${e(b.karta.izoh || "")}</textarea>
    <button class="tugma" id="dav" style="margin-top:14px">${e(t("Davom etish"))} →</button>
  </div></main>`;
  el.querySelectorAll(".siljish .chip").forEach(c => c.onclick = () => {
    titra(); el.querySelector(`input[data-k="${c.dataset.k}"]`).value = c.dataset.v;
  });
  $("#dav").onclick = () => {
    el.querySelectorAll("input[data-k]").forEach(i => { my[i.dataset.k] = i.value.trim(); });
    b.karta.izoh = $("#izoh").value.trim();
    const yoq = tur.maydonlar.find(f => !my[f.kalit]);
    if (yoq) { bildir(tc(yoq.savol), true); el.querySelector(`input[data-k="${yoq.kalit}"]`).focus(); return; }
    aiQadam3(el, tl, b);
  };
}

function aiQadam3(el, tl, b) {
  const tur = tl.turlar[b.karta.tur];
  const nom = { boy: "Bo'y", kokrak: "Ko'krak", bel: "Bel", son: "Son" };
  el.innerHTML = ichkiSarlavha(t("O'lchamlar va muddat")) + `<main><div class="karta">
    ${tur.olcham.length ? `
      <div class="qator wrap">
        <button class="tugma oq kichik" id="saql">📏 ${e(t("Saqlangan o'lchamlarim"))}</button>
        <button class="tugma tilla kichik" id="masl">🤖 ${e(t("O'lchamni maslahat bering"))}</button></div>
      ${b.olcham.razmer ? `<p style="margin-top:10px">✅ <b>${e(tc(b.olcham.razmer))}</b></p>` : ""}
      ${tur.olcham.map(k => `<label>${e(tc(nom[k]))} (sm)</label><input inputmode="numeric" data-o="${k}" value="${e(b.olcham[k] || "")}">`).join("")}`
      : `<p class="xira">✔️ ${e(tc("Bu mahsulot uchun tana o'lchami kerak emas."))}</p>`}
    <label>${e(t("Qachonga kerak?"))}</label><input id="mud" value="${e(b.muddat)}" placeholder="2 hafta">
    <label>${e(t("Telefon"))}</label><input id="tel" inputmode="tel" value="${e(b.tel)}" placeholder="+998">
    <button class="tugma" id="dav" style="margin-top:14px">${e(t("Davom etish"))} →</button>
  </div></main>`;
  const yigish = () => { el.querySelectorAll("input[data-o]").forEach(i => { if (i.value.trim()) b.olcham[i.dataset.o] = i.value.trim(); else delete b.olcham[i.dataset.o]; });
    b.muddat = $("#mud").value.trim(); b.tel = $("#tel").value.trim(); };
  const s = $("#saql");
  if (s) s.onclick = () => { const o = H.men.olchamlar || {};
    if (!Object.keys(o).length) return bildir(t("Topilmadi"), true);
    yigish(); Object.assign(b.olcham, o); aiQadam3(el, tl, b); };
  const m = $("#masl");
  if (m) m.onclick = () => { yigish(); maslahatVaraq(o => { Object.assign(b.olcham, o); aiQadam3(el, tl, b); }); };
  $("#dav").onclick = () => {
    yigish();
    if ((b.tel || "").replace(/\D/g, "").length < 7) return bildir(t("Telefon"), true);
    aiQadam4(el, tl, b);
  };
}
T["Bu mahsulot uchun tana o'lchami kerak emas."] = ["Bul ónim ushın dene ólshemi kerek emes.", "No body measurements needed for this item."];

function maslahatVaraq(tanlandi) {
  const v = varaq(`<main><h3 class="bolim-nom">🤖 ${e(t("O'lchamni maslahat bering"))}</h3>
    <div class="karta"><label>${e(t("Kim uchun?"))}</label>
    <div class="segment" id="jins"><button data-j="ayol" class="tan">${e(t("Ayol"))}</button><button data-j="erkak">${e(t("Erkak"))}</button><button data-j="bola">${e(t("Bola"))}</button></div>
    <label>${e(t("Bo'y (sm)"))}</label><input id="mB" inputmode="numeric">
    <label id="vL">${e(t("Vazn (kg)"))}</label><input id="mV" inputmode="numeric">
    <button class="tugma" id="mOl" style="margin-top:12px">${e(t("Maslahat olish"))}</button>
    <div id="mNat"></div></div></main>`);
  let jins = "ayol";
  v.querySelectorAll("#jins button").forEach(x => x.onclick = () => {
    jins = x.dataset.j; v.querySelectorAll("#jins button").forEach(y => y.classList.toggle("tan", y === x));
    $("#mV", v).hidden = $("#vL", v).hidden = jins === "bola"; });
  $("#mOl", v).onclick = () => urin(async () => {
    const r = await api("maslahat", { jins, boy: $("#mB", v).value, vazn: $("#mV", v).value });
    $("#mNat", v).innerHTML = `<p style="margin:12px 0">🤖 ${e(tc(r.izoh))}</p><div class="chiplar">${r.variantlar.map((x, i) =>
      `<button class="chip ${x.tavsiya ? "tan" : ""}" data-i="${i}">${e(tc(x.nom))}${x.tavsiya ? " ★" : ""}</button>`).join("")}</div>
      <p class="xira" style="margin-top:8px">${e(tc("Bu taxminiy tavsiya: aniq o'lchamni usta primerkada tekshiradi."))}</p>`;
    $("#mNat", v).querySelectorAll(".chip").forEach(c => c.onclick = () => {
      const x = r.variantlar[+c.dataset.i];
      const o = { razmer: x.nom };
      Object.entries(x.olcham).forEach(([k, val]) => { if (val) o[k] = String(val); });
      v.remove(); tanlandi(o);
    });
  });
}

function aiQadam4(el, tl, b) {
  const tur = tl.turlar[b.karta.tur];
  const qatorlar = tur.maydonlar.filter(f => b.karta.maydonlar[f.kalit]).map(f =>
    `<dt>${e(tc(tl.maydon_nomi[f.kalit] || f.kalit))}</dt><dd>${e(tc(b.karta.maydonlar[f.kalit]))}</dd>`).join("");
  const olch = Object.entries(b.olcham).map(([k, v]) => `${e(tc({ razmer: "O'lcham", boy: "Bo'y", kokrak: "Ko'krak", bel: "Bel", son: "Son" }[k] || k))}: ${e(tc(v))}`).join(", ");
  el.innerHTML = ichkiSarlavha(t("Buyurtma kartasi")) + `<main><div class="karta">
    <h3>📋 ${e(tc(tur.nom))}</h3><dl class="maydonlar">${qatorlar}
    ${olch ? `<dt>📏</dt><dd>${olch}</dd>` : ""}${b.muddat ? `<dt>🗓</dt><dd>${e(b.muddat)}</dd>` : ""}
    <dt>📞</dt><dd>${e(b.tel)}</dd>${b.karta.izoh ? `<dt>✏️</dt><dd>${e(b.karta.izoh)}</dd>` : ""}</dl>
    <p class="xira">${e(t("Narx va muddatni hunarmand taklif qiladi. AI narx o'ylab topmaydi."))}</p>
    <button class="tugma" id="yub" style="margin-top:14px">✅ ${e(t("Tasdiqlayman, yuborilsin"))}</button>
    <button class="tugma oq" id="tah" style="margin-top:8px">✏️ ${e(t("Orqaga"))}</button></div></main>`;
  $("#tah").onclick = () => aiQadam2(el, tl, b);
  $("#yub").onclick = () => urin(async () => {
    $("#yub").disabled = true;
    try {
      const r = await api("buyurtma", { karta: b.karta, olcham: b.olcham, muddat: b.muddat, tel: b.tel, dizayn: b.dizayn });
      H.men.tel = b.tel;
      try { tg && tg.HapticFeedback.notificationOccurred("success"); } catch (_) {}
      el.innerHTML = ichkiSarlavha(t("Buyurtma yuborildi!")) + `<main><div class="karta" style="text-align:center">
        <div style="font-size:54px">🎉</div><h3>${e(t("Buyurtma yuborildi!"))} #${e(r.raqam)}</h3>
        <p class="xira">${e(tc("Hunarmandlar narx va muddat taklif qilishadi — bot orqali ham xabar beramiz."))}</p>
        <button class="tugma" style="margin-top:14px" onclick="H.tarix=[];och('buyurtmalar')">📦 ${e(t("Buyurtmalar"))}</button></div></main>`;
    } catch (x) { $("#yub").disabled = false; throw x; }
  });
}

/* ---------------- Dizaynlar ---------------- */
async function dizaynlarOl() {
  if (!H.kesh.dz) H.kesh.dz = (await api("dizaynlar")).dizaynlar;
  return H.kesh.dz;
}

function tovarKarta(x, tur) {
  const kalit = (tur === "d" ? "d:" : "m:") + x.id;
  return `<div class="tovar" data-id="${e(x.id)}"><div class="r" style="background-image:url('${x.rasm}')"></div>
    ${tur === "d" ? `<span class="belgi">${e(t(x.uslub))}</span>` : ""}
    <button class="yurak" data-s="${e(kalit)}">${x.sevimli ? "❤️" : "🤍"}</button>
    <div class="i"><b>${e(tc(x.nom))}</b>${x.narx ? `<div class="narx">${pul(x.narx)}</div>` : ""}</div></div>`;
}

function yurakUla(el, royxat) {
  el.querySelectorAll(".yurak").forEach(y => y.onclick = ev => {
    ev.stopPropagation(); titra();
    urin(async () => {
      const r = await api("sevimli", { kalit: y.dataset.s });
      H.men.sevimlilar = r.sevimlilar;
      const x = royxat.find(z => (z.id === y.dataset.s.slice(2)));
      if (x) x.sevimli = !x.sevimli;
      y.textContent = r.sevimlilar.includes(y.dataset.s) ? "❤️" : "🤍";
    });
  });
}

SAHIFALAR.dizaynlar = async (el) => {
  const dz = await dizaynlarOl();
  let uslub = "*", kat = "*";
  const katlar = [...new Set(dz.map(d => d.kategoriya))];
  const chiz = () => {
    const r = dz.filter(d => (uslub === "*" || d.uslub === uslub) && (kat === "*" || d.kategoriya === kat));
    el.innerHTML = `<header class="bosh"><h1>👗 ${e(t("Dizaynlar"))}</h1><p>${e(tc("Yoqqanini tanlang — o'lchamingizga tikib beramiz"))}</p></header><div class="tasma"></div>
    <main><div class="segment">${[["*", "Hammasi"], ["O'zbek", "O'zbek"], ["Qoraqalpoq", "Qoraqalpoq"]].map(([k, n]) =>
      `<button data-u="${e(k)}" class="${uslub === k ? "tan" : ""}">${e(t(n))}</button>`).join("")}</div>
    <div class="siljish"><button class="chip ${kat === "*" ? "tan" : ""}" data-k="*">${e(t("Hammasi"))}</button>${katlar.map(k =>
      `<button class="chip ${kat === k ? "tan" : ""}" data-k="${e(k)}">${e(tc(k))}</button>`).join("")}</div>
    <div class="panjara">${r.map(d => tovarKarta(d, "d")).join("") || `<div class="bosh-holat"><span>🧵</span>${e(t("Topilmadi"))}</div>`}</div></main>`;
    el.querySelectorAll(".segment button").forEach(b => b.onclick = () => { uslub = b.dataset.u; chiz(); });
    el.querySelectorAll(".siljish .chip").forEach(b => b.onclick = () => { kat = b.dataset.k; chiz(); });
    el.querySelectorAll(".tovar").forEach(x => x.onclick = () => dizaynVaraq(dz.find(d => d.id === x.dataset.id)));
    yurakUla(el, dz);
  };
  chiz();
};
T["Yoqqanini tanlang — o'lchamingizga tikib beramiz"] = ["Unaǵanın saylań — ólshemińizge tigip beremiz", "Pick one — we'll tailor it to your size"];

function dizaynVaraq(d) {
  const v = varaq(`<img src="${d.rasm}" style="width:100%;max-height:60vh;object-fit:cover">
    <main><h3 class="bolim-nom">${e(tc(d.nom))}</h3><p>${e(tc(d.tavsif))}</p>
    <dl class="maydonlar">${d.mato ? `<dt>🧵</dt><dd>${e(tc(d.mato))}</dd>` : ""}${d.rang ? `<dt>🎨</dt><dd>${e(tc(d.rang))}</dd>` : ""}
    <dt>🏷</dt><dd>${e(t(d.uslub))} · ${e(tc(d.kategoriya))}</dd></dl>
    <button class="tugma" id="dzB">🧵 ${e(t("Shu dizaynda buyurtma"))}</button></main>`);
  $("#dzB", v).onclick = () => urin(async () => {
    const r = await api("dizayn_karta", { id: d.id });
    v.remove();
    och("ai", { karta: r.karta, dizayn: d.id }, true);
  });
}

/* ---------------- Do'kon va savat ---------------- */
SAHIFALAR.dokon = async (el) => {
  const [m, s] = await Promise.all([api("mahsulotlar"), api("savat", {})]);
  H.savat = s.savat.reduce((a, x) => a + x.soni, 0); nav();
  const ms = m.mahsulotlar;
  el.innerHTML = `<header class="bosh"><h1>🛍 ${e(t("Do'kon"))}</h1><p>${e(tc("Tayyor kiyimlar — uyingizgacha yetkazamiz"))}</p></header><div class="tasma"></div>
  <main><button class="tugma oq" id="savB">🛒 ${e(t("Savat"))} · ${H.savat}</button>
  <div class="panjara">${ms.map(x => tovarKarta(x, "m")).join("") || ""}</div>
  ${ms.length ? "" : `<div class="bosh-holat"><span>🛍</span>${e(tc("Hozircha sotuvda mahsulot yo'q. Tez orada tayyor kiyimlar joylanadi."))}</div>`}</main>`;
  $("#savB").onclick = () => och("savat", null, true);
  el.querySelectorAll(".tovar").forEach(x => x.onclick = () => mahsulotVaraq(ms.find(z => z.id === x.dataset.id)));
  yurakUla(el, ms);
};
T["Tayyor kiyimlar — uyingizgacha yetkazamiz"] = ["Tayar kiyimler — úyińizge shekem jetkeremiz", "Ready-made clothes, delivered to you"];

function mahsulotVaraq(m) {
  let olcham = null;
  const v = varaq(`${m.rasm ? `<img src="${m.rasm}" style="width:100%;max-height:55vh;object-fit:cover">` : ""}
    <main><h3 class="bolim-nom">${e(m.nom)}</h3><p>${e(m.tavsif)}</p>
    <p style="font:800 22px var(--sans);color:var(--qizil)">${pul(m.narx)}</p>
    <p class="xira">🏪 ${e(t("Sotuvchi"))}: ${e(m.sotuvchi)}</p>
    <label>${e(t("O'lchamni tanlang"))}</label>
    <div class="chiplar">${Object.entries(m.zaxira).map(([o, n]) => `<button class="chip" data-o="${e(o)}">${e(o)} · ${n}</button>`).join("")}</div>
    <button class="tugma" id="sB" style="margin-top:14px">🛒 ${e(t("Savatga"))}</button></main>`);
  v.querySelectorAll(".chip").forEach(c => c.onclick = () => { olcham = c.dataset.o; v.querySelectorAll(".chip").forEach(x => x.classList.toggle("tan", x === c)); });
  $("#sB", v).onclick = () => {
    if (!olcham) return bildir(t("O'lchamni tanlang"), true);
    urin(async () => { const r = await api("savat", { amal: "qosh", id: m.id, olcham });
      H.savat = r.savat.reduce((a, x) => a + x.soni, 0); nav(); v.remove(); bildir("🛒 " + t("Savatga") + " ✓");
      if (H.sahifa === "dokon") $("#savB").textContent = "🛒 " + t("Savat") + " · " + H.savat; });
  };
}

SAHIFALAR.savat = async (el) => {
  const chiz = (s) => {
    H.savat = s.savat.reduce((a, x) => a + x.soni, 0); nav();
    if (!s.savat.length) { el.innerHTML = ichkiSarlavha(t("Savat")) + `<div class="bosh-holat"><span>🛒</span>${e(t("Savat bo'sh"))}</div>`; return; }
    el.innerHTML = ichkiSarlavha(t("Savat")) + `<main>${s.savat.map(x => `<div class="karta qator">
      ${x.rasm ? `<img src="${x.rasm}" style="width:64px;height:80px;object-fit:cover;border-radius:10px">` : ""}
      <div style="flex:1"><b>${e(x.nom)}</b><div class="xira">${e(x.olcham)} · ${pul(x.narx)}</div>
      <div class="qator" style="margin-top:6px"><button class="tugma oq kichik" data-a="kam" data-i="${x.indeks}">−</button><b>${x.soni}</b>
      <button class="tugma oq kichik" data-a="kop" data-i="${x.indeks}">+</button><button class="tugma oq kichik" data-a="och" data-i="${x.indeks}">🗑</button></div></div></div>`).join("")}
      <div class="karta"><div class="qator ora"><span>${e(t("Mahsulotlar"))}</span><b>${pul(s.jami)}</b></div>
      <div class="qator ora"><span>${e(t("Yetkazish"))}</span><b>${s.yetkazish ? pul(s.yetkazish) : e(t("bepul"))}</b></div><hr>
      <div class="qator ora"><span>${e(t("Jami"))}</span><b style="color:var(--qizil)">${pul(s.jami + s.yetkazish)}</b></div>
      <div class="segment" id="usul" style="margin-top:12px"><button data-u="yetkazish" class="tan">🚚 ${e(t("Yetkazib berish"))}</button><button data-u="olib">🏪 ${e(t("O'zim olib ketaman"))}</button></div>
      <div id="mzW"><label>${e(t("Manzil"))}</label><input id="mz" value="${e(H.men.manzil || "")}"></div>
      <label>${e(t("Telefon"))}</label><input id="tel" inputmode="tel" value="${e(H.men.tel || "")}" placeholder="+998">
      <button class="tugma" id="ras" style="margin-top:14px">✅ ${e(t("Rasmiylashtirish"))}</button></div></main>`;
    let usul = "yetkazish";
    el.querySelectorAll("#usul button").forEach(b => b.onclick = () => { usul = b.dataset.u;
      el.querySelectorAll("#usul button").forEach(x => x.classList.toggle("tan", x === b)); $("#mzW").hidden = usul === "olib"; });
    el.querySelectorAll("[data-a]").forEach(b => b.onclick = () => urin(async () => chiz(await api("savat", { amal: b.dataset.a, indeks: +b.dataset.i }))));
    $("#ras").onclick = () => urin(async () => {
      const r = await api("rasmiylashtir", { usul, manzil: $("#mz").value, tel: $("#tel").value });
      H.men.tel = $("#tel").value; H.savat = 0; H.tarix = [];
      och("buyurtmalar", { tab: "sotuv", ochiq: r.raqam });
    });
  };
  chiz(await api("savat", {}));
};

/* ---------------- Buyurtmalar ---------------- */
SAHIFALAR.buyurtmalar = async (el, p) => {
  const r = await api("buyurtmalarim");
  let tab = (p && p.tab) || "tikish";
  const chiz = () => {
    const royxat = tab === "tikish" ? r.tikish : r.sotuv;
    el.innerHTML = `<header class="bosh"><h1>📦 ${e(t("Buyurtmalar"))}</h1></header><div class="tasma"></div><main>
      <div class="segment"><button data-t="tikish" class="${tab === "tikish" ? "tan" : ""}">🪡 ${e(t("Tikish"))} (${r.tikish.length})</button>
      <button data-t="sotuv" class="${tab === "sotuv" ? "tan" : ""}">🛍 ${e(t("Do'kon"))} (${r.sotuv.length})</button></div>
      ${royxat.length ? royxat.map(b => tab === "tikish" ? tikishKarta(b) : sotuvKarta(b)).join("")
        : `<div class="bosh-holat"><span>📦</span>${e(t("Hali buyurtma yo'q"))}<br><br><button class="tugma" style="width:auto" onclick="och('ai',null,true)">🤖 ${e(t("AI bilan buyurtma"))}</button></div>`}</main>`;
    el.querySelectorAll(".segment button").forEach(b => b.onclick = () => { tab = b.dataset.t; chiz(); });
    tikishUla(el, r);
  };
  chiz();
};

function yol(b) {
  return `<div class="yol">${b.kuzatuv.map(q => `<div class="qadam ${q.holat}"><i>${q.holat === "otdi" ? "✓" : q.holat === "joriy" ? "●" : ""}</i>
    <div><b>${e(tc(q.nom))}</b>${q.vaqt && q.holat !== "keyin" ? `<small>${e(q.vaqt)}</small>` : ""}</div></div>`).join("")}</div>`;
}

function ustaQator(u) {
  return `<div class="qator ora"><div><b>🪡 ${e(u.ism)}</b>${u.shahar ? ` · <span class="xira">${e(u.shahar)}</span>` : ""}
    <div class="xira"><span class="yulduz">${u.baholar ? "★".repeat(Math.round(u.reyting)) + " " + u.reyting : "☆"}</span> · ✅ ${u.bajarilgan}</div></div></div>
    ${u.portfolio.length ? `<div class="portf">${u.portfolio.map(x => `<img src="${x}" data-k="${x}">`).join("")}</div>` : ""}`;
}

function tikishKarta(b) {
  const S = H.men.sozlama;
  let amal = "";
  if (b.holat === "yangi") {
    amal = b.takliflar.length ? `<h3 style="margin-top:12px">💬 ${e(t("Takliflar"))} (${b.takliflar.length})</h3>${b.takliflar.map(x => `<div class="taklif">
      ${ustaQator(x.usta)}<p style="margin:6px 0"><b style="color:var(--qizil);font-size:18px">${pul(x.narx)}</b> · 🗓 ${x.kun} ${e(tc("kun"))}</p>
      ${x.izoh ? `<p class="xira">💬 ${e(x.izoh)}</p>` : ""}
      <div class="qator wrap" style="margin-top:8px"><button class="tugma kichik" data-tanla="${e(x.usta_id)}" data-r="${b.raqam}">✅ ${e(t("Tanlash"))}</button>
      <button class="tugma oq kichik" data-yoz="${e(x.usta_id)}" data-r="${b.raqam}">❓ ${e(t("Savol berish"))}</button>
      ${x.usta.sharhlar && x.usta.sharhlar.length ? `<button class="tugma oq kichik" data-sh="${e(x.usta_id)}" data-r="${b.raqam}">💬 ${e(t("Sharhlar"))}</button>` : ""}</div></div>`).join("")}`
      : `<p class="xira" style="margin-top:8px">⏳ ${e(t("Takliflar kutilmoqda"))}</p>`;
  }
  const tolov = (tur, summa) => `<div class="taklif"><b>💳 ${e(t("To'lov"))}: ${pul(summa)}</b>
    <p class="xira">${e(t("Karta"))}:</p><div class="qator ora"><span class="kod">${e(S.karta)}</span>
    <button class="tugma oq kichik" data-nusxa="${e(S.karta)}">📋</button></div><p class="xira">${e(S.karta_egasi)}</p>
    ${b.tolov.holat.endsWith("tekshiruvda") ? `<p style="margin-top:8px">🔍 ${e(tc("Chek tekshirilmoqda"))}</p>`
      : `<button class="tugma" style="margin-top:10px" data-chek="${tur}" data-r="${b.raqam}">📸 ${e(t("Chek rasmini yuborish"))}</button>`}</div>`;
  if (b.holat === "tasdiqlangan") amal = tolov("oldindan", b.tolov.oldindan);
  if (b.holat === "tayyor") amal = tolov("qolgan", b.tolov.qolgan);
  if (b.holat === "yetkazilmoqda") amal = `<button class="tugma" style="margin-top:10px" data-olindi="${b.raqam}">✅ ${e(t("Qabul qilib oldim"))}</button>`;
  if (b.holat === "yakunlandi" && !b.baho && b.usta) amal = `<div class="taklif"><b>${e(t("Baholang"))}</b>
    <div class="yulduz-tanla" data-r="${b.raqam}">${[1, 2, 3, 4, 5].map(i => `<button data-b="${i}">⭐</button>`).join("")}</div>
    <textarea placeholder="${e(t("Sharh yozing"))}" data-shm="${b.raqam}"></textarea>
    <button class="tugma" style="margin-top:8px" data-baho="${b.raqam}">${e(t("Yuborish"))}</button></div>`;
  const yozish = b.usta && ["tasdiqlangan", "tikilmoqda", "tayyor", "yetkazilmoqda"].includes(b.holat)
    ? `<button class="tugma oq kichik" data-yoz="${e(b.usta.id)}" data-r="${b.raqam}">✉️ ${e(t("Hunarmandga yozish"))}</button>` : "";
  const bekor = ["yangi", "tasdiqlangan"].includes(b.holat) && !b.tolov.holat.endsWith("tekshiruvda")
    ? `<button class="tugma oq kichik" data-bekor="${b.raqam}">❌ ${e(t("Bekor qilish"))}</button>` : "";
  return `<div class="karta"><div class="qator ora"><h3>#${b.raqam} · ${e(tc(b.mahsulot))}</h3>${b.narx ? `<b>${pul(b.narx)}</b>` : ""}</div>
    <span class="holat">${e(tc(b.holat_nomi))}</span>
    ${b.tayyor_rasm || b.dizayn_rasm ? `<img src="${b.tayyor_rasm || b.dizayn_rasm}" style="margin-top:10px;border-radius:12px;max-height:220px;object-fit:cover;width:100%">` : ""}
    <details style="margin-top:8px"><summary class="xira">📋 ${e(t("Buyurtma kartasi"))}</summary><dl class="maydonlar">
    ${b.maydonlar.map(m => `<dt>${e(tc(m.nom))}</dt><dd>${e(tc(m.qiymat))}</dd>`).join("")}
    ${Object.entries(b.olcham).filter(([k, v]) => v && v !== "-").map(([k, v]) => `<dt>${e(oN(k))}</dt><dd>${e(tc(v))}</dd>`).join("")}</dl></details>
    ${b.usta ? `<div style="margin-top:8px">${ustaQator(b.usta)}</div>` : ""}
    ${yol(b)}${amal}<div class="qator wrap" style="margin-top:8px">${yozish}${bekor}</div></div>`;
}
T["kun"] = ["kún", "days"]; T["Chek tekshirilmoqda"] = ["Chek tekserilmekte", "Receipt is being checked"];

function sotuvKarta(s) {
  const S = H.men.sozlama;
  return `<div class="karta"><div class="qator ora"><h3>#${s.raqam}</h3><b>${pul(s.umumiy)}</b></div>
    <span class="holat">${e(tc(s.holat_nomi))}</span>
    <p style="margin-top:8px">${s.mahsulotlar.map(m => `• ${e(m.nom)} · ${e(m.olcham)} · ${m.soni}`).join("<br>")}</p>
    <p class="xira">${s.usul === "olib" ? "🏪 " + e(t("O'zim olib ketaman")) : "📍 " + e(s.manzil)}</p>
    ${s.holat === "tolov_kutilmoqda" ? `<div class="taklif"><p class="xira">${e(t("Karta"))}:</p><div class="qator ora"><span class="kod">${e(S.karta)}</span>
      <button class="tugma oq kichik" data-nusxa="${e(S.karta)}">📋</button></div><p class="xira">${e(S.karta_egasi)}</p>
      <button class="tugma" style="margin-top:10px" data-chek="sotuv" data-r="${s.raqam}">📸 ${e(t("Chek rasmini yuborish"))}</button></div>` : ""}</div>`;
}

function tikishUla(el, r) {
  const qayta = () => och("buyurtmalar", { tab: H.param && H.param.tab });
  el.querySelectorAll("[data-tanla]").forEach(b => b.onclick = () => urin(async () => {
    if (tg && tg.showConfirm) { const ha = await new Promise(o => tg.showConfirm(t("Tanlash") + "?", o)); if (!ha) return; }
    await api("taklif_tanla", { raqam: b.dataset.r, usta: b.dataset.tanla }); qayta(); }));
  el.querySelectorAll("[data-chek]").forEach(b => b.onclick = async () => {
    const rasm = await rasmTanla(); if (!rasm) return;
    b.disabled = true; b.textContent = "⏳ …";
    urin(async () => { await api("chek", { raqam: b.dataset.r, tur: b.dataset.chek, rasm }); bildir("✅"); qayta(); })
      .catch(() => { b.disabled = false; b.textContent = "📸 " + t("Chek rasmini yuborish"); });
  });
  el.querySelectorAll("[data-nusxa]").forEach(b => b.onclick = () => {
    navigator.clipboard && navigator.clipboard.writeText(b.dataset.nusxa.replace(/\s/g, "")); bildir("📋 ✓"); });
  el.querySelectorAll("[data-olindi]").forEach(b => b.onclick = () => urin(async () => { await api("olindi", { raqam: b.dataset.olindi }); qayta(); }));
  el.querySelectorAll("[data-bekor]").forEach(b => b.onclick = async () => {
    if (tg && tg.showConfirm) { const ha = await new Promise(o => tg.showConfirm(t("Bekor qilish") + "?", o)); if (!ha) return; }
    urin(async () => { await api("bekor", { raqam: b.dataset.bekor }); qayta(); }); });
  el.querySelectorAll(".yulduz-tanla").forEach(w => w.querySelectorAll("button").forEach(b => b.onclick = () => {
    w.dataset.ball = b.dataset.b; w.querySelectorAll("button").forEach(x => x.classList.toggle("yon", +x.dataset.b <= +b.dataset.b)); titra(); }));
  el.querySelectorAll("[data-baho]").forEach(b => b.onclick = () => {
    const w = el.querySelector(`.yulduz-tanla[data-r="${b.dataset.baho}"]`);
    if (!w.dataset.ball) return bildir(t("Baholang"), true);
    urin(async () => { await api("baho", { raqam: b.dataset.baho, ball: +w.dataset.ball, matn: el.querySelector(`[data-shm="${b.dataset.baho}"]`).value });
      bildir("🙏"); qayta(); });
  });
  el.querySelectorAll("[data-yoz]").forEach(b => b.onclick = () => {
    const v = varaq(`<main><h3 class="bolim-nom">✉️ ${e(t("Xabar"))}</h3><textarea id="yM"></textarea>
      <button class="tugma" id="yB" style="margin-top:10px">${e(t("Yuborish"))}</button></main>`);
    $("#yB", v).onclick = () => urin(async () => { await api("yoz", { raqam: b.dataset.r, usta: b.dataset.yoz, matn: $("#yM", v).value });
      v.remove(); bildir("✅ " + t("Telegramga yubordik")); });
  });
  el.querySelectorAll("[data-sh]").forEach(b => b.onclick = () => {
    const bb = r.tikish.find(x => x.raqam === b.dataset.r);
    const u = bb.takliflar.find(x => x.usta_id === b.dataset.sh).usta;
    sharhVaraq(u);
  });
  el.querySelectorAll(".portf img").forEach(i => i.onclick = ev => { ev.stopPropagation(); varaq(`<img src="${i.dataset.k}" style="width:100%">`); });
}

function sharhVaraq(u) {
  varaq(`<main><h3 class="bolim-nom">💬 ${e(u.ism)}</h3>${ustaQator(u)}${(u.sharhlar || []).map(s => `<div class="karta">
    <span class="yulduz">${"★".repeat(s.baho)}</span> <span class="xira">${e(s.sana)} · ${e(s.mijoz)}</span>
    ${s.matn ? `<p>«${e(s.matn)}»</p>` : ""}</div>`).join("") || `<p class="xira">—</p>`}</main>`);
}

/* ---------------- Kataloglar ---------------- */
async function katOl() {
  if (!H.kesh.kat) H.kesh.kat = await api("kataloglar");
  return H.kesh.kat;
}

SAHIFALAR.matolar = async (el) => {
  const k = await katOl();
  el.innerHTML = ichkiSarlavha("🧵 " + t("Matolar")) + `<main>${k.matolar.map(m => `<details class="mato"><summary>${e(tc(m.nom))}</summary><div>
    <p><b>${e(t("Tarkibi"))}:</b> ${e(tc(m.tarkib))}</p><p style="margin:6px 0">${e(tc(m.xususiyat))}</p>
    <p>✂️ <b>${e(t("Mos kiyimlar"))}:</b> ${e(tc(m.mos))}</p><p>🧼 <b>${e(t("Parvarish"))}:</b> ${e(tc(m.parvarish))}</p>
    <button class="tugma kichik" style="margin-top:10px" data-m="${e(m.kod)}">🤖 ${e(t("Shu matodan buyurtma"))}</button></div></details>`).join("")}</main>`;
  el.querySelectorAll("[data-m]").forEach(b => b.onclick = () =>
    och("ai", { karta: { tur: null, maydonlar: { mato: b.dataset.m, material: b.dataset.m }, izoh: "" } }, true));
};

SAHIFALAR.olchamlar = async (el) => {
  const k = await katOl();
  let tur = "ayol";
  const chiz = () => {
    const jad = tur === "bola"
      ? `<tr><th>${e(t("Bo'y (sm)"))}</th><th>${e(tc("Ko'krak"))}</th><th>${e(tc("Bel"))}</th><th>${e(tc("Son"))}</th></tr>` +
        k.olcham.bola.map(r => `<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td></tr>`).join("")
      : `<tr><th>RU</th><th>INT</th><th>${e(tc("Ko'krak"))}</th><th>${e(tc("Bel"))}</th><th>${e(tc("Son"))}</th></tr>` +
        k.olcham[tur].map(r => `<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td><td>${r[4]}</td></tr>`).join("");
    el.innerHTML = ichkiSarlavha("📐 " + t("O'lchamlar")) + `<main>
      <div class="segment">${[["ayol", "Ayol"], ["erkak", "Erkak"], ["bola", "Bola"]].map(([a, n]) =>
        `<button data-t="${a}" class="${tur === a ? "tan" : ""}">${e(t(n))}</button>`).join("")}</div>
      <div class="karta"><table class="olch">${jad}</table><p class="xira" style="margin-top:8px">sm</p></div>
      <div class="karta"><h3>📏 ${e(tc("O'zingizni qanday o'lchaysiz"))}</h3><p>${e(tc(
        "Ko'krak — eng bo'rtgan joyidan, bel — eng ingichka joyidan, son — eng keng joyidan o'lchanadi. Lentani tortmang va bo'sh ham qo'ymang."))}</p></div>
      <button class="tugma tilla" id="msl">🤖 ${e(t("O'lchamni maslahat bering"))}</button></main>`;
    el.querySelectorAll(".segment button").forEach(b => b.onclick = () => { tur = b.dataset.t; chiz(); });
    $("#msl").onclick = () => maslahatVaraq(o => urin(async () => {
      const r = await api("profil", { olchamlar: o }); H.men = Object.assign(H.men, r); bildir("✅ " + t("Saqlandi") + ": " + tc(o.razmer)); }));
  };
  chiz();
};
T["O'zingizni qanday o'lchaysiz"] = ["Ózińizdi qalay ólsheysiz", "How to measure yourself"];

SAHIFALAR.akademiya = async (el, hunar) => {
  const k = await katOl();
  if (!hunar) {
    el.innerHTML = ichkiSarlavha("🎓 " + t("Akademiya")) + `<main>${k.hunarlar.map(h => `<div class="karta qator ora" data-h="${e(h)}" style="cursor:pointer">
      <b>${e(tc(h))}</b><span class="xira">${k.darslar.filter(d => d.hunar === h).length} ▸</span></div>`).join("")}</main>`;
    el.querySelectorAll("[data-h]").forEach(x => x.onclick = () => och("akademiya", x.dataset.h, true));
    return;
  }
  const ds = k.darslar.filter(d => d.hunar === hunar);
  el.innerHTML = ichkiSarlavha("🎓 " + tc(hunar)) + `<main>${ds.length ? ds.map(d => `<div class="karta"><h3>▶️ ${e(d.nom)}</h3>
    ${d.tavsif ? `<p class="xira">${e(d.tavsif)}</p>` : ""}<div class="qator" style="margin-top:8px">
    ${d.havola ? `<button class="tugma kichik" data-l="${e(d.havola)}">${e(t("Ochish"))}</button>` : ""}
    ${d.video ? `<button class="tugma kichik" data-v="${d.id}">📲 ${e(t("Telegramga yuborish"))}</button>` : ""}</div></div>`).join("")
    : `<div class="bosh-holat"><span>🎓</span>${e(t("Darslar tez orada"))}<br><br>
       <button class="tugma oq" style="width:auto" data-l="${e(k.qidiruv[hunar])}">▶️ ${e(t("YouTube'da ko'rish"))}</button></div>`}</main>`;
  el.querySelectorAll("[data-l]").forEach(b => b.onclick = () => tg && tg.openLink ? tg.openLink(b.dataset.l) : window.open(b.dataset.l));
  el.querySelectorAll("[data-v]").forEach(b => b.onclick = () => urin(async () => { await api("dars_video", { id: +b.dataset.v }); bildir("✅ " + t("Telegramga yubordik")); }));
};

SAHIFALAR.ustalar = async (el) => {
  const r = await api("ustalar");
  el.innerHTML = ichkiSarlavha("🪡 " + t("Hunarmandlar")) + `<main>${r.ustalar.map((u, i) => `<div class="karta">${ustaQator(u)}
    <p class="xira">${e(u.ixtisos)}${u.tajriba ? " · " + e(u.tajriba) + " " + e(tc("yil")) : ""}${u.pauza ? " · ⏸" : ""}</p>
    ${u.sharhlar.length ? `<button class="tugma oq kichik" style="margin-top:8px" data-i="${i}">💬 ${e(t("Sharhlar"))} (${u.sharhlar.length})</button>` : ""}</div>`).join("")
    || `<div class="bosh-holat"><span>🪡</span>${e(t("Topilmadi"))}</div>`}</main>`;
  el.querySelectorAll("[data-i]").forEach(b => b.onclick = () => sharhVaraq(r.ustalar[+b.dataset.i]));
  el.querySelectorAll(".portf img").forEach(i => i.onclick = () => varaq(`<img src="${i.dataset.k}" style="width:100%">`));
};
T["yil"] = ["jıl", "years"];

SAHIFALAR.qidiruv = async (el, soz) => {
  const q = (soz || "").toLowerCase();
  const [dz, m, k] = await Promise.all([dizaynlarOl(), api("mahsulotlar"), katOl()]);
  const mos = s => String(s || "").toLowerCase().includes(q);
  const d1 = dz.filter(d => mos(d.nom) || mos(d.tavsif) || mos(d.mato) || mos(d.kategoriya));
  const m1 = m.mahsulotlar.filter(x => mos(x.nom) || mos(x.tavsif) || mos(x.kategoriya));
  const t1 = k.matolar.filter(x => mos(x.nom) || mos(x.mos) || mos(x.xususiyat));
  el.innerHTML = ichkiSarlavha("🔍 «" + soz + "»") + `<main>
    <input id="qid" value="${e(soz)}">
    ${d1.length ? `<div class="bolim-nom">👗 ${e(t("Dizaynlar"))}</div><div class="panjara">${d1.map(d => tovarKarta(d, "d")).join("")}</div>` : ""}
    ${m1.length ? `<div class="bolim-nom">🛍 ${e(t("Do'kon"))}</div><div class="panjara" id="mP">${m1.map(x => tovarKarta(x, "m")).join("")}</div>` : ""}
    ${t1.length ? `<div class="bolim-nom">🧵 ${e(t("Matolar"))}</div>${t1.map(x => `<div class="karta" data-t="1"><b>${e(tc(x.nom))}</b><p class="xira">${e(tc(x.mos))}</p></div>`).join("")}` : ""}
    ${d1.length + m1.length + t1.length ? "" : `<div class="bosh-holat"><span>🔍</span>${e(t("Topilmadi"))}</div>`}</main>`;
  $("#qid").onkeydown = ev => { if (ev.key === "Enter") och("qidiruv", ev.target.value.trim()); };
  el.querySelectorAll(".tovar").forEach(x => x.onclick = () => {
    const d = dz.find(z => z.id === x.dataset.id); d ? dizaynVaraq(d) : mahsulotVaraq(m1.find(z => z.id === x.dataset.id)); });
  el.querySelectorAll("[data-t]").forEach(x => x.onclick = () => och("matolar", null, true));
  yurakUla(el, d1.concat(m1));
};

SAHIFALAR.sevimlilar = async (el) => {
  const [dz, m] = await Promise.all([dizaynlarOl(), api("mahsulotlar")]);
  const s = H.men.sevimlilar || [];
  const d1 = dz.filter(d => s.includes("d:" + d.id)), m1 = m.mahsulotlar.filter(x => s.includes("m:" + x.id));
  el.innerHTML = ichkiSarlavha("❤️ " + t("Sevimlilar")) + `<main>${d1.length + m1.length
    ? `<div class="panjara">${d1.map(d => tovarKarta(Object.assign({}, d, { sevimli: true }), "d")).join("")}${m1.map(x => tovarKarta(Object.assign({}, x, { sevimli: true }), "m")).join("")}</div>`
    : `<div class="bosh-holat"><span>🤍</span>${e(t("Topilmadi"))}</div>`}</main>`;
  el.querySelectorAll(".tovar").forEach(x => x.onclick = () => {
    const d = dz.find(z => z.id === x.dataset.id); d ? dizaynVaraq(d) : mahsulotVaraq(m1.find(z => z.id === x.dataset.id)); });
  yurakUla(el, d1.concat(m1));
};

/* ---------------- Men: profil ---------------- */
const TILLAR = [["uz", "O'zbekcha (lotin)"], ["uz_cyr", "Ўзбекча (кирилл)"], ["kaa", "Qaraqalpaqsha (latın)"],
  ["kaa_cyr", "Қарақалпақша (кирилл)"], ["en", "English"]];

SAHIFALAR.men = async (el) => {
  const m = H.men;
  const o = m.olchamlar || {};
  el.innerHTML = `<header class="bosh"><h1>👤 ${e(m.ism || t("Men"))}</h1><p>${m.admin ? "🛠 Admin · " : ""}${m.rol === "usta" ? "🪡 " + e(t("Hunarmand")) : ""}</p></header><div class="tasma"></div>
  <main>
    ${m.admin ? `<button class="tugma" onclick="och('admin',null,true)">🛠 ${e(t("Admin paneli"))}</button>` : ""}
    ${m.rol === "usta" && m.tasdiq ? `<button class="tugma tilla" onclick="och('usta',null,true)">🪡 ${e(t("Hunarmand paneli"))}</button>` : ""}
    <div class="tez">
      <button onclick="och('sevimlilar',null,true)"><span>❤️</span>${e(t("Sevimlilar"))}</button>
      <button onclick="och('ustalar',null,true)"><span>🪡</span>${e(t("Hunarmandlar"))}</button>
      <button onclick="och('akademiya',null,true)"><span>🎓</span>${e(t("Akademiya"))}</button></div>
    <div class="karta"><h3>${e(t("Men"))}</h3>
      <label>${e(t("Ism"))}</label><input id="pI" value="${e(m.ism)}">
      <label>${e(t("Telefon"))}</label><input id="pT" inputmode="tel" value="${e(m.tel)}">
      <label>${e(t("Manzil"))}</label><input id="pM" value="${e(m.manzil)}">
      <label>${e(t("Til"))}</label><select id="pL">${TILLAR.map(([k, n]) => `<option value="${k}" ${m.til === k ? "selected" : ""}>${n}</option>`).join("")}</select>
      <h3 style="margin-top:16px">📏 ${e(t("Saqlangan o'lchamlarim"))}</h3>
      <div class="panjara">${["razmer", "boy", "kokrak", "bel", "son"].map(k => `<div><label>${e(tc({ razmer: "O'lcham", boy: "Bo'y", kokrak: "Ko'krak", bel: "Bel", son: "Son" }[k]))}</label>
        <input data-o="${k}" value="${e(o[k] || "")}"></div>`).join("")}</div>
      <button class="tugma" id="pS" style="margin-top:14px">💾 ${e(t("Saqlash"))}</button></div>
    ${m.rol !== "usta" ? `<div class="karta"><h3>🪡 ${e(t("Hunarmand bo'lish"))}</h3>
      <p class="xira">${e(tc("Ariza yuboring — tasdiqlangach buyurtmalar sizga keladi."))}</p>
      <button class="tugma oq" id="uB" style="margin-top:10px">${e(t("Ariza yuborish"))}</button></div>`
      : !m.tasdiq ? `<div class="karta">⏳ ${e(t("Ariza ko'rib chiqilmoqda"))}</div>` : ""}
    <div class="karta"><h3>📞 ${e(t("Operatorga yozish"))}</h3><textarea id="opM"></textarea>
      <button class="tugma oq" id="opB" style="margin-top:8px">${e(t("Yuborish"))}</button>
      <p class="xira" style="margin-top:10px">${e(m.sozlama.tel)} · ${e(m.sozlama.tg)}</p></div>
  </main>`;
  $("#pS").onclick = () => urin(async () => {
    const olch = {}; el.querySelectorAll("[data-o]").forEach(i => { if (i.value.trim()) olch[i.dataset.o] = i.value.trim(); });
    const yangiTil = $("#pL").value, tilO = yangiTil !== m.til;
    H.men = Object.assign(H.men, await api("profil", { ism: $("#pI").value, tel: $("#pT").value, manzil: $("#pM").value, til: yangiTil, olchamlar: olch }));
    bildir("✅ " + t("Saqlandi"));
    if (tilO) { H.kesh = {}; H.turlar = null; och("men"); }
  });
  $("#opB").onclick = () => urin(async () => { await api("operator", { matn: $("#opM").value }); $("#opM").value = ""; bildir("✅ " + t("Telegramga yubordik")); });
  const ub = $("#uB");
  if (ub) ub.onclick = () => {
    const v = varaq(`<main><h3 class="bolim-nom">🪡 ${e(t("Hunarmand bo'lish"))}</h3><div class="karta">
      ${[["ism", "Ism"], ["shahar", "Shahar"], ["ixtisos", "Nima tikasiz?"], ["tajriba", "Tajriba (yil)"], ["tel", "Telefon"]].map(([k, n]) =>
        `<label>${e(t(n))}</label><input data-u="${k}" value="${e(k === "ism" ? m.ism : k === "tel" ? m.tel : "")}">`).join("")}
      <button class="tugma" id="uY" style="margin-top:12px">${e(t("Ariza yuborish"))}</button></div></main>`);
    $("#uY", v).onclick = () => urin(async () => {
      const d = {}; v.querySelectorAll("[data-u]").forEach(i => d[i.dataset.u] = i.value);
      H.men = Object.assign(H.men, await api("usta/royxat", d)); v.remove(); och("men"); });
  };
};
T["Ariza yuboring — tasdiqlangach buyurtmalar sizga keladi."] = ["Arza jiberiń — tastıyıqlanǵannan keyin buyırtpalar sizge keledi.", "Apply — once approved, orders will come to you."];

/* ---------------- Hunarmand paneli ---------------- */
SAHIFALAR.usta = async (el) => {
  const r = await api("usta/buyurtmalar");
  const u = r.men;
  el.innerHTML = ichkiSarlavha("🪡 " + t("Hunarmand paneli")) + `<main>
    <div class="plitka"><div><b>${u.reyting || "—"}</b><small>★ · ${u.baholar} ${e(t("baho"))}</small></div>
      <div><b>${u.bajarilgan}</b><small>${e(t("Bajarilgan ishlar"))}</small></div>
      <div><b style="font-size:16px">${pul(r.daromad)}</b><small>${e(t("Ishlab topilgan"))}</small></div>
      <div style="cursor:pointer" id="pz"><b>${r.pauza ? "⏸" : "▶️"}</b><small>${e(t("Dam olish"))}: ${r.pauza ? "ON" : "OFF"}</small></div></div>
    <div class="bolim-nom">🆕 ${e(t("Yangi buyurtmalar"))} (${r.ochiq.length})</div>
    ${r.ochiq.map(b => `<div class="karta"><h3>#${b.raqam} · ${e(tc(b.mahsulot))}</h3>
      ${b.dizayn_rasm ? `<img src="${b.dizayn_rasm}" style="border-radius:12px;max-height:200px;object-fit:cover;width:100%;margin:6px 0">` : ""}
      <dl class="maydonlar">${b.maydonlar.map(m => `<dt>${e(tc(m.nom))}</dt><dd>${e(tc(m.qiymat))}</dd>`).join("")}
      ${Object.entries(b.olcham).filter(([k, v]) => v && v !== "-").map(([k, v]) => `<dt>${e(oN(k))}</dt><dd>${e(v)}</dd>`).join("")}${b.muddat ? `<dt>🗓</dt><dd>${e(b.muddat)}</dd>` : ""}</dl>
      <div class="qator"><button class="tugma kichik" data-tk="${b.raqam}">💰 ${e(t("Narx taklif qilish"))}</button>
      <button class="tugma oq kichik" data-rad="${b.raqam}">❌ ${e(t("Rad etish"))}</button></div></div>`).join("") || `<p class="xira">—</p>`}
    ${r.takliflarim.length ? `<div class="bolim-nom">⏳ ${e(t("Takliflar"))}</div>${r.takliflarim.map(b => `<div class="karta qator ora">
      <span>#${b.raqam} · ${e(tc(b.mahsulot))}</span><b>${pul(b.mening_taklif.narx)} · ${b.mening_taklif.kun} ${e(tc("kun"))}</b></div>`).join("")}` : ""}
    <div class="bolim-nom">🧾 ${e(t("Mening ishlarim"))}</div>
    ${r.ishlar.map(b => `<div class="karta"><div class="qator ora"><h3>#${b.raqam} · ${e(tc(b.mahsulot))}</h3><b>${pul(b.usta_narx)}</b></div>
      <span class="holat">${e(tc(b.holat_nomi))}</span>${b.mijoz_tel ? `<p class="xira" style="margin-top:6px">📞 ${e(b.mijoz_tel)}</p>` : ""}
      <details><summary class="xira">📋 ${e(t("Buyurtma kartasi"))}</summary><dl class="maydonlar">${b.maydonlar.map(m => `<dt>${e(tc(m.nom))}</dt><dd>${e(tc(m.qiymat))}</dd>`).join("")}
      ${Object.entries(b.olcham).filter(([k, v]) => v && v !== "-").map(([k, v]) => `<dt>${e(oN(k))}</dt><dd>${e(v)}</dd>`).join("")}</dl></details>
      <div class="qator wrap" style="margin-top:8px">${b.holat === "tikilmoqda" ? `<button class="tugma kichik" data-tay="${b.raqam}">✅ ${e(t("Tayyor bo'ldi"))}</button>` : ""}
      ${["tasdiqlangan", "tikilmoqda", "tayyor", "yetkazilmoqda"].includes(b.holat) ? `<button class="tugma oq kichik" data-yoz="${b.raqam}">✉️ ${e(t("Xabar"))}</button>` : ""}</div></div>`).join("") || `<p class="xira">—</p>`}
    <div class="bolim-nom">🖼 ${e(t("Portfolio"))} (${u.portfolio.length}/10)</div>
    <div class="portf">${u.portfolio.map(x => `<img src="${x}">`).join("")}</div>
    <div class="qator"><button class="tugma kichik" id="pfQ">➕ ${e(t("Rasm qo'shish"))}</button>
      ${u.portfolio.length ? `<button class="tugma oq kichik" id="pfT">🗑</button>` : ""}</div>
    ${u.sharhlar.length ? `<div class="bolim-nom">💬 ${e(t("Sharhlar"))}</div>${u.sharhlar.map(s => `<div class="karta"><span class="yulduz">${"★".repeat(s.baho)}</span>
      <span class="xira">${e(s.sana)} · ${e(s.mijoz)}</span>${s.matn ? `<p>«${e(s.matn)}»</p>` : ""}</div>`).join("")}` : ""}
  </main>`;
  const qayta = () => och("usta");
  $("#pz").onclick = () => urin(async () => { await api("usta/pauza"); qayta(); });
  el.querySelectorAll("[data-rad]").forEach(b => b.onclick = () => urin(async () => { await api("usta/rad", { raqam: b.dataset.rad }); qayta(); }));
  el.querySelectorAll("[data-tk]").forEach(b => b.onclick = () => {
    const v = varaq(`<main><h3 class="bolim-nom">💰 #${b.dataset.tk}</h3><div class="karta">
      <label>${e(t("Narx (mato + mehnat), so'm"))}</label><input id="tN" inputmode="numeric">
      <p class="xira" id="tM"></p>
      <label>${e(t("Necha kun"))}</label><input id="tK" inputmode="numeric">
      <label>${e(t("Izoh"))}</label><textarea id="tI"></textarea>
      <button class="tugma" id="tY" style="margin-top:12px">${e(t("Yuborish"))}</button></div></main>`);
    const S = H.men.sozlama;
    $("#tN", v).oninput = ev => { const n = +ev.target.value.replace(/\D/g, "");
      $("#tM", v).textContent = n ? tc("Mijozga ko'rinadi: ") + pul(Math.ceil(n / (1 - S.komissiya / 100) / 5000) * 5000) : ""; };
    $("#tY", v).onclick = () => urin(async () => {
      await api("usta/taklif", { raqam: b.dataset.tk, narx: +$("#tN", v).value.replace(/\D/g, ""), kun: +$("#tK", v).value.replace(/\D/g, ""), izoh: $("#tI", v).value });
      v.remove(); bildir("✅"); qayta(); });
  });
  el.querySelectorAll("[data-tay]").forEach(b => b.onclick = async () => {
    const rasm = await rasmTanla();
    urin(async () => { await api("usta/tayyor", { raqam: b.dataset.tay, rasm }); qayta(); });
  });
  el.querySelectorAll("[data-yoz]").forEach(b => b.onclick = () => {
    const v = varaq(`<main><h3 class="bolim-nom">✉️ #${b.dataset.yoz}</h3><textarea id="yM"></textarea>
      <button class="tugma" id="yB" style="margin-top:10px">${e(t("Yuborish"))}</button></main>`);
    $("#yB", v).onclick = () => urin(async () => { await api("yoz", { raqam: b.dataset.yoz, matn: $("#yM", v).value }); v.remove(); bildir("✅"); });
  });
  $("#pfQ").onclick = async () => { const rasm = await rasmTanla(); if (rasm) urin(async () => { await api("usta/portfolio", { rasm }); qayta(); }); };
  const pt = $("#pfT"); if (pt) pt.onclick = () => urin(async () => { await api("usta/portfolio", { amal: "toza" }); qayta(); });
};
T["Mijozga ko'rinadi: "] = ["Klientke kórinedi: ", "Customer sees: "];

/* ---------------- Admin paneli ---------------- */
SAHIFALAR.admin = async (el, tab) => {
  const r = await api("admin/holat");
  const s = r.stat;
  tab = tab || "tolov";
  const TAB = [["tolov", "💳 " + t("To'lovlar") + " (" + r.tolovlar.length + ")"], ["buyurtma", "🪡 " + t("Buyurtmalar")],
    ["dokon", "🛍 " + t("Do'kon")], ["usta", "🪡 " + t("Hunarmandlar") + (s.kutayotgan ? " (" + s.kutayotgan + ")" : "")],
    ["foyd", "👥 " + t("Foydalanuvchilar")], ["qosh", "➕ " + t("Qo'shish")]];
  let ich = "";
  if (tab === "tolov") ich = r.tolovlar.map(x => `<div class="karta"><div class="qator ora"><h3>#${x.raqam} · ${x.tur === "sotuv" ? "🛍" : x.chek_tur === "oldindan" ? "1/2" : "2/2"}</h3><b>${pul(x.summa)}</b></div>
      ${x.rasm ? `<img src="${x.rasm}" style="border-radius:12px;margin:8px 0;max-height:320px;object-fit:contain;width:100%;background:#0001">` : `<p class="xira">(fayl)</p>`}
      <div class="qator"><button class="tugma kichik" data-am="${x.tur === "sotuv" ? "tolangan" : "tolov_ha"}" data-id="${x.raqam}" data-ct="${x.chek_tur || ""}">✅ ${e(t("Tasdiqlash"))}</button>
      <button class="tugma oq kichik" data-am="${x.tur === "sotuv" ? "bekor_s" : "tolov_yoq"}" data-id="${x.raqam}">❌ ${e(t("Rad"))}</button></div></div>`).join("") || `<p class="xira">—</p>`;
  if (tab === "buyurtma") ich = r.buyurtmalar.map(b => `<div class="karta"><div class="qator ora"><h3>#${b.raqam} · ${e(b.mahsulot)}</h3>${b.narx ? `<b>${pul(b.narx)}</b>` : ""}</div>
      <span class="holat">${e(b.holat_nomi)}</span>${b.usta ? `<p class="xira">🪡 ${e(b.usta.ism)}</p>` : ""}
      ${b.holat === "yetkazilmoqda" ? `<button class="tugma kichik" style="margin-top:8px" data-am="topshirildi" data-id="${b.raqam}">📦 ${e(t("Topshirildi"))}</button>` : ""}</div>`).join("") || `<p class="xira">—</p>`;
  if (tab === "dokon") ich = r.sotuvlar.map(x => `<div class="karta"><div class="qator ora"><h3>#${x.raqam}</h3><b>${pul(x.umumiy)}</b></div>
      <span class="holat">${e(x.holat_nomi)}</span><p class="xira">${x.mahsulotlar.map(m => e(m.nom) + " · " + e(m.olcham) + " · " + m.soni).join("<br>")}</p>
      <p class="xira">📞 ${e(x.tel)} ${x.manzil ? "· 📍 " + e(x.manzil) : "· 🏪"}</p><div class="qator wrap" style="margin-top:6px">
      ${x.holat === "tolangan" ? `<button class="tugma kichik" data-am="yolda" data-id="${x.raqam}">🚚 ${e(t("Yo'lga chiqdi"))}</button>` : ""}
      ${["tolangan", "yolda"].includes(x.holat) ? `<button class="tugma kichik" data-am="topshirildi_s" data-id="${x.raqam}">✅ ${e(t("Topshirildi"))}</button>` : ""}
      <button class="tugma oq kichik" data-am="bekor_s" data-id="${x.raqam}">❌</button></div></div>`).join("") || `<p class="xira">—</p>`;
  if (tab === "usta") ich = r.ustalar.sort((a, b) => a.tasdiq - b.tasdiq).map(u => `<div class="karta">${ustaQator(u)}
      <p class="xira">${e(u.ixtisos)} · ${e(u.tajriba)} · 📞 ${e(u.tel)} ${u.username ? "· @" + e(u.username) : ""}</p>
      <p>${u.bloklangan ? "🚫" : u.tasdiq ? "✅" : "⏳"}</p><div class="qator wrap" style="margin-top:6px">
      ${!u.tasdiq ? `<button class="tugma kichik" data-am="usta_tasdiq" data-id="${u.id}">✅ ${e(t("Tasdiqlash"))}</button>
        <button class="tugma oq kichik" data-am="usta_rad" data-id="${u.id}">❌ ${e(t("Rad"))}</button>` : ""}
      <button class="tugma oq kichik" data-am="blok" data-id="${u.id}">${u.bloklangan ? "✅" : "🚫 " + e(t("Bloklash"))}</button></div></div>`).join("") || `<p class="xira">—</p>`;
  if (tab === "foyd") ich = `<input id="fQ" placeholder="🔍">` + `<div id="fR">${r.foydalanuvchilar.map(u => `<div class="karta" data-q="${e((u.ism + " " + u.username + " " + u.tel + " " + u.id).toLowerCase())}">
      <div class="qator ora"><b>${e(u.ism || "—")}</b><span class="xira">${e(u.til)}</span></div>
      <p class="xira">${u.username ? "@" + e(u.username) + " · " : ""}${e(u.tel)} · 📦 ${u.buyurtma} · 🕒 ${e(u.oxirgi)}</p>
      <div class="qator" style="margin-top:6px">${u.username ? `<button class="tugma oq kichik" data-l="https://t.me/${e(u.username)}">💬</button>` : ""}
      <button class="tugma oq kichik" data-am="blok" data-id="${u.id}">${u.bloklangan ? "✅" : "🚫"}</button></div></div>`).join("")}</div>`;
  if (tab === "qosh") ich = `<div class="karta"><div class="segment" id="qT"><button data-q="mahsulot" class="tan">🛍</button><button data-q="dizayn">👗</button><button data-q="dars">🎓</button></div>
      <div id="qF"></div></div>
      <div class="karta"><h3>👗/🛍</h3>${r.dizaynlar.concat(r.mahsulotlar).map(x => `<div class="qator ora"><span>${e(x.id)} · ${e(x.nom)}</span>
      <button class="tugma oq kichik" data-am="${x.id[0] === "M" ? "mahsulot_faol" : "dizayn_faol"}" data-id="${e(x.id)}">${x.faol ? "👁" : "🚫"}</button></div>`).join("")}</div>
      <button class="tugma tilla" id="zx">💾 ${e(t("Zaxira olish"))}</button>`;
  el.innerHTML = ichkiSarlavha("🛠 " + t("Admin paneli")) + `<main>
    <div class="plitka"><div><b>${s.foydalanuvchi}</b><small>👥 ${e(t("Foydalanuvchilar"))}</small></div><div><b>${s.buyurtma}</b><small>🪡 ${e(t("Buyurtmalar"))} · ✅ ${s.yakunlangan}</small></div>
      <div><b style="font-size:16px">${pul(s.foyda)}</b><small>💰 foyda · ${pul(s.aylanma)}</small></div><div><b style="font-size:16px">${pul(s.dokon_aylanma)}</b><small>🛍 ${e(t("Do'kon"))} · ${s.sotuv}</small></div></div>
    <div class="siljish">${TAB.map(([k, n]) => `<button class="chip ${tab === k ? "tan" : ""}" data-tab="${k}">${e(n)}</button>`).join("")}</div>
    ${ich}</main>`;
  const qayta = () => och("admin", tab);
  el.querySelectorAll("[data-tab]").forEach(b => b.onclick = () => och("admin", b.dataset.tab));
  el.querySelectorAll("[data-am]").forEach(b => b.onclick = () => urin(async () => {
    await api("admin/amal", { amal: b.dataset.am, id: b.dataset.id, chek_tur: b.dataset.ct }); bildir("✅"); qayta(); }));
  el.querySelectorAll("[data-l]").forEach(b => b.onclick = () => tg && tg.openTelegramLink ? tg.openTelegramLink(b.dataset.l) : window.open(b.dataset.l));
  const fq = $("#fQ"); if (fq) fq.oninput = () => el.querySelectorAll("#fR [data-q]").forEach(x => x.hidden = !x.dataset.q.includes(fq.value.toLowerCase()));
  const zx = $("#zx"); if (zx) zx.onclick = () => urin(async () => { await api("admin/zaxira"); bildir("✅ " + t("Telegramga yubordik")); });
  if (tab === "qosh") {
    let qt = "mahsulot", rasm = null;
    const forma = () => {
      const f = { mahsulot: [["nom", "Nomi"], ["tavsif", "Tavsif"], ["kategoriya", "Kategoriya"], ["narx", "Narx"], ["zaxira", "S:2, M:3, L:1"], ["sotuvchi", "Sotuvchi"]],
        dizayn: [["nom", "Nomi"], ["tavsif", "Tavsif"], ["kategoriya", "Kategoriya"], ["uslub", "O'zbek / Qoraqalpoq"], ["mato", "Mato"], ["rang", "Rang"], ["kiyim", "ko'ylak / sumka / nimcha ..."]],
        dars: [["nom", "Nomi"], ["tavsif", "Tavsif"], ["hunar", "Kashtachilik / Zardo'zlik / Ko'rpachado'zlik / Tikuvchilik / Boshqa hunarlar"], ["havola", "https://..."]] }[qt];
      $("#qF").innerHTML = f.map(([k, n]) => `<label>${e(t(n))}</label><input data-f="${k}" placeholder="${e(n)}">`).join("")
        + (qt !== "dars" ? `<button class="tugma oq" id="qR" style="margin-top:10px">📷 ${e(t("Rasm"))}</button>` : "")
        + `<button class="tugma" id="qY" style="margin-top:10px">➕ ${e(t("Qo'shish"))}</button>`;
      const qr = $("#qR"); if (qr) qr.onclick = async () => { rasm = await rasmTanla(); if (rasm) qr.textContent = "📷 ✓"; };
      $("#qY").onclick = () => urin(async () => { const d = { tur: qt, rasm }; el.querySelectorAll("[data-f]").forEach(i => d[i.dataset.f] = i.value.trim());
        if (qt === "dizayn" && /^q/i.test(d.uslub || "")) d.uslub = "Qoraqalpoq";
        const r2 = await api("admin/qosh", d); H.kesh = {}; bildir("✅ " + r2.id); qayta(); });
    };
    el.querySelectorAll("#qT button").forEach(b => b.onclick = () => { qt = b.dataset.q; el.querySelectorAll("#qT button").forEach(x => x.classList.toggle("tan", x === b)); forma(); });
    forma();
  }
};

/* ---------------- Ishga tushirish ---------------- */
(async function boshla() {
  try {
    if (tg) {
      tg.ready(); tg.expand();
      try { tg.setHeaderColor("#7E0B15"); tg.setBackgroundColor(getComputedStyle(document.body).backgroundColor); } catch (_) {}
      tg.BackButton.onClick(orqaga);
    }
    const dev = new URLSearchParams(location.search).get("dev");
    const r = await fetch("/api/kirish", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ initData: tg ? tg.initData : "", dev_uid: dev }) });
    const j = await r.json();
    if (!r.ok) throw new Error(j.xato || "Xato");
    H.men = j; H.token = j.token;
    document.documentElement.lang = j.til.startsWith("en") ? "en" : "uz";
    const start = tg && tg.initDataUnsafe && tg.initDataUnsafe.start_param;
    och(start && SAHIFALAR[start] ? start : "bosh");
    api("savat", {}).then(s => { H.savat = s.savat.reduce((a, x) => a + x.soni, 0); nav(); }).catch(() => {});
  } catch (x) {
    $("#ilova").innerHTML = `<div class="bosh-holat"><span>🧵</span><b>Chevar AI</b><br>${e(x.message)}<br><br>
      <a href="https://t.me/chevarai_bot">@chevarai_bot</a></div>`;
  }
})();
