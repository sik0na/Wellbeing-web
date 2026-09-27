# content.py - all the texts the app shows for each emotion.
# The model only picks the KEY (e.g. "worried"); these texts were written
# and checked by people, so the app never says something unsafe.

EMOTIONS = {
    "worried": {
        "name": "Fear / worry",
        "emoji": "😟",
        "message": "It makes sense to feel worried when something matters to you. "
                   "Try to focus on one small thing you can do today.",
    },
    "sad": {
        "name": "Sadness",
        "emoji": "😢",
        "message": "Feeling sad is hard, and you don't have to push it away. "
                   "Be gentle with yourself today.",
    },
    "angry": {
        "name": "Anger / frustration",
        "emoji": "😠",
        "message": "Feeling angry is a normal reaction when something feels unfair. "
                   "A few slow breaths or a short walk can help.",
    },
    "stressed": {
        "name": "Stress / overwhelm",
        "emoji": "😩",
        "message": "You have a lot going on. You don't have to do it all at once. "
                   "Pick just one small next task.",
    },
    "lonely": {
        "name": "Loneliness",
        "emoji": "🫂",
        "message": "Feeling lonely is very common among students. "
                   "A small step, like messaging someone, can help.",
    },
    "happy": {
        "name": "Happiness",
        "emoji": "😊",
        "message": "That's great to hear! Take a moment to notice what went well today.",
    },
    "calm": {
        "name": "Calm / okay",
        "emoji": "😌",
        "message": "It's good to have a steady day. Enjoy the calm.",
    },
}