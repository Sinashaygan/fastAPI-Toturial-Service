from core.database import SessionLocal
from core.models import User

db = SessionLocal()

try:
    user = User(
        first_name="Ali",
        last_name="Ahmadi",
        age=31,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"User saved: {user}")
finally:
    db.close()
