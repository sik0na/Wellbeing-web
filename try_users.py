import database

database.create_tables()
print("new user id:", database.create_user("anna", "sunflower123"))
print("same name again:", database.create_user("anna", "other"))
print("right password:", database.check_login("anna", "sunflower123") is not None)
print("wrong password:", database.check_login("anna", "wrong") is not None)