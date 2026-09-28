import database

database.create_tables()
database.save_checkin("I'm worried about my exams", "worried", "worried")
database.save_checkin("I miss home", "sad", "lonely")

for row in database.get_all_checkins():
    print(row["id"], row["created_at"], row["text"], "→", row["chosen"])