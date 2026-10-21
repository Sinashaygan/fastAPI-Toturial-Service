from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    age = Column(Integer)

    def __repr__(self):
        return (
            f"User(id={self.id}, first_name='{self.first_name}', "
            f"last_name='{self.last_name}')"
        )
