from core.database import Base, engine
from core import models

Base.metadata.create_all(bind=engine)

print("Database and tables created successfully.")
