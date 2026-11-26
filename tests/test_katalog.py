import sys, os, tempfile
P=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,P)
import tempfile; D_=tempfile.mkdtemp(); os.makedirs(D_,exist_ok=True); os.environ["DATA_DIR"]=D_
for f in os.listdir(D_): os.remove(D_+"/"+f)
os.chdir(P)
import core
core.AI_CFG={"ai_provider":"yoq","ai_key":"","ai_model":"","ai_url":""}
LOG=[]
def fake(m,**p):
    kb=p.get("reply_markup") or {}
    LOG.append((m,p.get("chat_id"),p.get("text") or p.get("caption") or "",[(b["text"],b.get("callback_data")) for r in kb.get("inline_keyboard",[])+kb.get("keyboard",[]) for b in r]))
    return {"ok":True,"result":{"message_id":1}}
core.api=fake; core.rasm_yuklash=lambda c,y:"F"
import bot, katalog; bot.api=fake; bot.AI_CFG=core.AI_CFG
def msg(u,t=None,video=None):
    m={"chat":{"type":"private"},"from":{"id":u,"first_name":"Ali"},"message_id":1}
    if video: m["video"]={"file_id":video}
    else: m["text"]=t
    bot.xabar(m)
def cb(u,d): bot.tugma({"id":"1","from":{"id":u},"data":d,"message":{"message_id":1}})
def ok(c,n): print(("✅ " if c else "❌ ")+n)
def last(u): return [x for x in LOG if x[1]==u][-1]
D=core.DATA; A=5939503983; M=101
for u in (M,A): msg(u,"/start"); cb(u,"til_uz")
ok(any(t=="📚 Kataloglar" for t,_ in last(M)[3]),"Menyuda «📚 Kataloglar»")
msg(M,"📚 Kataloglar"); ok(len(last(M)[3])==3,"Kataloglar: matolar, o'lchamlar, akademiya")
cb(M,"kt_mato"); ok(len(last(M)[3])==8,"8 ta mato")
cb(M,"mt_beqasam"); ok("chapon" in last(M)[2] and "Tarkibi" in last(M)[2],"Mato kartasi: xususiyat va mos kiyim")
cb(M,"mtb_adras"); k=D["holatlar"][str(M)]["karta"]; ok(k["maydonlar"].get("mato")=="adras" and last(M)[2].startswith("❓"),"«Shu matodan buyurtma» → mato oldindan yozildi")
cb(M,"tur_ko'ylak"); ok("Qaysi matodan" not in "".join(x[2] for x in LOG[-3:]),"Mato qayta so'ralmadi")
cb(M,"kt_olcham"); cb(M,"oj_ayol"); ok("48 L" in last(M)[2] and "96" in last(M)[2],"Ayollar jadvali")
cb(M,"oj_bola"); ok("128" in last(M)[2],"Bolalar jadvali")
# buyurtma + maslahat
msg(M,"Menga ko'k adras zamonaviy ko'ylak kerak to'yga")
for x in ["uzun","uzun yeng","tik yoqa"]: msg(M,x)
cb(M,"v_ok"); ok(any(c=="msb" for _,c in last(M)[3]),"O'lcham savolida «Maslahat bering» tugmasi")
cb(M,"msb"); cb(M,"ms_ayol"); msg(M,"163"); msg(M,"64")
v=last(M); print("   ",v[2].replace("\n"," | ")[:230]); print("   ",[t for t,_ in v[3]])
ok(sum("tavsiya" in t for t,_ in v[3])==1 and len(v[3])==4,"AI 3 variant va tavsiya berdi")
c=[c for t,c in v[3] if "tavsiya" in t][0]; cb(M,c)
o=D["holatlar"][str(M)]["olcham"]; print("   olcham:",o)
ok(o.get("razmer","").startswith("48") and o.get("boy")=="163" and "96" in o.get("kokrak",""),"Tanlangan o'lcham yozildi")
ok("qachonga" in last(M)[2],"Keyin muddatga o'tdi")
msg(M,"2 hafta"); msg(M,"+998901234567"); ok("O'lcham:</b> 48" in last(M)[2] or "48 (L)" in last(M)[2],"Yakuniy kartada o'lcham ko'rinadi")
# akademiya
cb(M,"kt_akad"); ok(len(last(M)[3])==5,"Akademiya: 5 hunar")
cb(M,"ak_1"); ok("youtube.com/results" in last(M)[2],"Dars yo'q bo'lsa — YouTube qidiruvi")
cb(A,"kt_dq"); cb(A,"dq_1"); msg(A,"Zardo'zlik: 1-dars"); msg(A,"-"); msg(A,video="VID1")
ok(D["darslar"] and D["darslar"][0]["video"]=="VID1","Admin video dars qo'shdi")
cb(M,"ak_1"); ok(any(x[0]=="sendVideo" and x[1]==M for x in LOG),"Mijoz videoni ko'rdi")
cb(M,"kt_dq"); ok(len(D["darslar"])==1 and D["holatlar"].get(str(M),{}).get("bosqich")!="dars","Mijoz dars qo'sha olmaydi")
