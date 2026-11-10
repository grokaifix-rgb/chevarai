# -*- coding: utf-8 -*-
"""
Lotin ⇄ kirill harf almashtirish (AI kerak emas, aniq qoida bilan).
  kiril_uz  — o'zbek lotin  → o'zbek kirill   (ko'ylak → кўйлак)
  kiril_kaa — qoraqalpoq lotin → qoraqalpoq kirill (Sebetińiz → Себетиңиз)
  lotin_uz  — kirillda yozilgan matnni lotinga (bot ichida tushunish uchun)
HTML teglar, @username, /buyruq, havola va <code> ichi o'zgarmaydi.
"""
import re

_TUTUQ = "'’‘ʻʼ`"
_HIMOYA = re.compile(r"(<code>.*?</code>|<[^>]+>|https?://\S+|tg://\S+|@\w+|/[a-z_]+|⟦\d+⟧|&\w+;|\bAI\b|\bUZS\b)", re.S)

_UZ_KOP = [("o" + t, "ў") for t in _TUTUQ] + [("g" + t, "ғ") for t in _TUTUQ] + [
    ("sh", "ш"), ("ch", "ч"), ("yo", "ё"), ("yu", "ю"), ("ya", "я"), ("ye", "е"), ("ts", "ц")]
_UZ_BIR = dict(zip("abdefghijklmnopqrstuvxyz",
                   "абдефгҳижклмнопқрстувхйз"))
_KAA_KOP = [("sh", "ш"), ("ch", "ч"), ("yo", "ё"), ("yu", "ю"), ("ya", "я"), ("ye", "е")]
_KAA_BIR = dict(zip("abdefghijklmnopqrstuvwxyzáóúıńǵ",
                    "абдефгҳижклмнопқрстувўхйзәөүыңғ"))
_UNLI_LOT = set("aeiouáóúıAEIOUÁÓÚI")


def _bolak(matn, kop, bir, e_bosh):
    natija = []
    i = 0
    n = len(matn)
    while i < n:
        ch = matn[i]
        past = matn[i:i + 2].lower()
        topildi = None
        for lat, kir in kop:
            # "yo'l" — bu ё emas, й + ў
            if past == lat and not (lat == "yo" and i + 2 < n and matn[i + 2] in _TUTUQ):
                topildi = (kir, 2)
                break
        if topildi:
            kir, uz = topildi
            if matn[i].isupper():
                kir = kir.upper() if (i + 2 >= n or not matn[i + 1].islower()) else kir.capitalize()
            natija.append(kir)
            i += uz
            continue
        low = ch.lower()
        if low == "e" and e_bosh:
            oldingi = matn[i - 1] if i else " "
            k = "э" if (not oldingi.isalpha() or oldingi in _UNLI_LOT) else "е"
        elif ch in _TUTUQ and i and matn[i - 1].isalpha() and i + 1 < n and matn[i + 1].isalpha():
            k = "ъ"
        elif low in bir:
            k = bir[low]
        else:
            natija.append(ch)
            i += 1
            continue
        natija.append(k.upper() if ch.isupper() else k)
        i += 1
    return "".join(natija)


def _qollash(matn, kop, bir, e_bosh):
    if not matn:
        return matn
    qismlar = _HIMOYA.split(matn)
    return "".join(q if _HIMOYA.fullmatch(q) else _bolak(q, kop, bir, e_bosh) for q in qismlar)


def kiril_uz(matn):
    return _qollash(matn, _UZ_KOP, _UZ_BIR, True)


def kiril_kaa(matn):
    return _qollash(matn, _KAA_KOP, _KAA_BIR, True)


_LOT = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "j", "з": "z",
        "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
        "с": "s", "т": "t", "у": "u", "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh",
        "ъ": "'", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya", "ў": "o'", "қ": "q", "ғ": "g'",
        "ҳ": "h", "ә": "a", "ө": "o", "ү": "u", "ң": "n", "і": "i"}


def lotin_uz(matn):
    """Kirill matnni lotinga (oddiy, tushunish uchun yetarli)."""
    if not matn or not re.search("[А-Яа-яЎўҚқҒғҲҳ]", matn):
        return matn
    q = []
    for ch in matn:
        l = _LOT.get(ch.lower())
        if l is None:
            q.append(ch)
        else:
            q.append(l.capitalize() if ch.isupper() else l)
    return "".join(q)
