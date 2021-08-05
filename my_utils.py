from replit import db

def delete_database():
  keys = db.keys()
  for k in keys:
    del db[k]
