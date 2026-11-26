"""Sinovlar uchun umumiy tayyorgarlik: soxta Telegram, vaqtinchalik baza, AI o'chiq."""
import os, sys, tempfile
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, P)
os.environ["DATA_DIR"] = tempfile.mkdtemp()
os.chdir(P)
import core
core.AI_CFG = {"ai_provider": "yoq", "ai_key": "", "ai_model": "", "ai_url": ""}
LOG = []
XATO = []


def fake(m, **p):
    kb = p.get("reply_markup") or {}
    LOG.append((m, p.get("chat_id"), p.get("text") or p.get("caption") or "",
                [(b["text"], b.get("callback_data")) for r in kb.get("inline_keyboard", []) + kb.get("keyboard", []) for b in r]))
    if m == "getFile":
        return {"ok": True, "result": {"file_path": "x.json"}}
    return {"ok": True, "result": {"message_id": 1}}


core.api = fake
core.rasm_yuklash = lambda c, y: "F_" + os.path.basename(y)
import bot  # noqa
bot.api = fake
bot.AI_CFG = core.AI_CFG
D = core.DATA
A = 5939503983


def msg(u, t=None, **qosh):
    m = {"chat": {"type": "private"}, "from": {"id": u, "first_name": "Ali"}, "message_id": 1}
    m.update(qosh)
    if t is not None:
        m["text"] = t
    bot.xabar(m)


def cb(u, d):
    bot.tugma({"id": "1", "from": {"id": u}, "data": d, "message": {"message_id": 1}})


def ok(c, n):
    print(("✅ " if c else "❌ ") + n)
    if not c:
        XATO.append(n)


def oxirgi(u):
    return [x for x in LOG if x[1] == u][-1]


def matnlar(u, n=60):
    return "\n".join(x[2] for x in [x for x in LOG if x[1] == u][-n:])
