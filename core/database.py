from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# آدرس اتصال به دیتابیس SQLite (یک فایل به نام sqlite.db در پروژه می‌سازد)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

# ایجاد موتور دیتابیس (Engine)
# نکته: آرگومان check_same_thread برای SQLite ضروری است تا اجازه کار با چند ترد را بدهد
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# ایجاد کلاس SessionLocal برای ساخت نشست‌ها (Sessions) جهت ارتباط با دیتابیس
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ساخت کلاس پایه (Base) که مدل‌های دیتابیس (Tables) از آن ارث‌بری خواهند کرد
Base = declarative_base()
