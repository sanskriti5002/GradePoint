import database, models
from routes.auth import get_password_hash

db = database.SessionLocal()
students = db.query(models.Student).all()
added = 0
for s in students:
    user = db.query(models.User).filter(models.User.username == s.email).first()
    if not user:
        new_user = models.User(
            username=s.email,
            hashed_password=get_password_hash(s.roll_number),
            role='student'
        )
        db.add(new_user)
        added += 1

db.commit()
db.close()
print(f'Backfilled {added} missing user accounts.')
