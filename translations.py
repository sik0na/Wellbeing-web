LANGUAGES = {
    "en": "English",
    "hu": "Magyar",
    "mn": "Монгол",
}

ROWS = [
    ("How are you today?", "Hogy vagy ma?", "Өнөөдөр ямар байна?"),
    ("Log in", "Bejelentkezés", "Нэвтрэх"),
    ("Log out", "Kijelentkezés", "Гарах"),
    ("Username", "Felhasználónév", "Хэрэглэгчийн нэр"),
    ("Password", "Jelszó", "Нууц үг"),
    ("Hi! How are you feeling today?", "Szia! Hogy érzed magad ma?", "Сайн уу! Өнөөдөр сэтгэл санаа тань ямар байна?"),
    ("Type a message…", "Írj üzenetet…", "Мессеж бичих…"),
    ("Send", "Küldés", "Илгээх"),
    ('Does "{emotion}" fit how you feel?', "Illik rád ez: „{emotion}”?", "“{emotion}” таны мэдрэмжид тохирч байна уу?"),
    ("Yes", "Igen", "Тийм"),
    ("Or pick another:", "Vagy válassz másikat:", "Эсвэл өөр нэгийг сонгоно уу:"),
    ("Save this check-in", "Bejegyzés mentése", "Тэмдэглэлийг хадгалах"),
    ("No thanks", "Nem, köszönöm", "Үгүй, баярлалаа"),
    ("Saved ✓ Anything else on your mind?", "Elmentve ✓ Van még valami a fejedben?", "Хадгалагдлаа ✓ Өөр бодогдож байгаа зүйл байна уу?"),
    ("Okay, not saved. Anything else on your mind?", "Rendben, nem mentettem el. Van még valami a fejedben?", "За, хадгалсангүй. Өөр бодогдож байгаа зүйл байна уу?"),
    ("Your history", "Előzmények", "Таны түүх"),
    ("No check-ins yet.", "Még nincs bejegyzés.", "Одоогоор тэмдэглэл алга."),
]

TRANSLATIONS = {"hu": {}, "mn": {}}
for english , hungarian , mongolian in ROWS:
    TRANSLATIONS["hu"][english] = hungarian
    TRANSLATIONS["mn"][english] = mongolian