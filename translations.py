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
        # ----- Emotions (from content.py) -----
    ("Fear / worry", "Félelem / aggodalom", "Айдас / санаа зоволт"),
    ("Sadness", "Szomorúság", "Гуниг"),
    ("Anger / frustration", "Düh / frusztráció", "Уур / бухимдал"),
    ("Stress / overwhelm", "Stressz / túlterheltség", "Стресс / дарамт"),
    ("Loneliness", "Magány", "Ганцаардал"),
    ("Happiness", "Boldogság", "Баяр баясгалан"),
    ("Calm / okay", "Nyugalom / rendben", "Тайван / зүгээр"),

    # ----- Supportive messages (from content.py) -----
    ("It makes sense to feel worried when something matters to you. Try to focus on one small thing you can do today.",
     "Érthető, hogy aggódsz, amikor valami fontos neked. Próbálj egy kis dologra figyelni, amit ma meg tudsz tenni.",
     "Танд чухал зүйлийн талаар санаа зовох нь ойлгомжтой. Өнөөдөр хийж чадах нэг жижиг зүйлдээ анхаараарай."),
    ("Feeling sad is hard, and you don't have to push it away. Be gentle with yourself today.",
     "Szomorúnak lenni nehéz, és nem kell elnyomnod ezt az érzést. Légy ma kedves magadhoz.",
     "Гунигтай байх хэцүү, энэ мэдрэмжээ түлхэн зайлуулах шаардлагагүй. Өнөөдөр өөртөө зөөлөн хандаарай."),
    ("Feeling angry is a normal reaction when something feels unfair. A few slow breaths or a short walk can help.",
     "A düh normális reakció, ha valami igazságtalannak tűnik. Néhány lassú légzés vagy egy rövid séta segíthet.",
     "Ямар нэг зүйл шударга бус санагдахад уурлах нь хэвийн. Хэдэн удаан амьсгаа эсвэл богино алхалт тусалж болно."),
    ("You have a lot going on. You don't have to do it all at once. Pick just one small next task.",
     "Sok minden van most rajtad. Nem kell mindent egyszerre megcsinálnod. Válassz egyetlen kis következő feladatot.",
     "Танд одоо олон зүйл байна. Бүгдийг нэг дор хийх шаардлагагүй. Дараагийн нэг жижиг ажлаа л сонгоорой."),
    ("Feeling lonely is very common among students. A small step, like messaging someone, can help.",
     "A magány nagyon gyakori a hallgatók között. Egy kis lépés, például egy üzenet valakinek, segíthet.",
     "Ганцаардах нь оюутнуудын дунд маш түгээмэл. Хэн нэгэнд мессеж бичих гэх мэт жижиг алхам тусалж болно."),
    ("That's great to hear! Take a moment to notice what went well today.",
     "Ezt jó hallani! Szánj egy percet arra, hogy észrevedd, mi sikerült ma jól.",
     "Сонсоход сайхан байна! Өнөөдөр юу сайн болсныг анзаарах хором гаргаарай."),
    ("It's good to have a steady day. Enjoy the calm.",
     "Jó, ha egy nyugodt napod van. Élvezd a nyugalmat.",
     "Тайван өдөр байх сайхан. Энэ тайван байдлыг мэдэрч таашаагаарай."),
]

TRANSLATIONS = {"hu": {}, "mn": {}}
for english , hungarian , mongolian in ROWS:
    TRANSLATIONS["hu"][english] = hungarian
    TRANSLATIONS["mn"][english] = mongolian
def translate(text, lang):
    return TRANSLATIONS.get(lang, {}).get(text, text)