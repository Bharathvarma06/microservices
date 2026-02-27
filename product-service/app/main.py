import time
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

from app.database import Base, engine
from app.routes import router

app = FastAPI(title="Auth Service")

@app.on_event("startup")
def startup():
    retries = 20   # ⬅️ increased
    while retries > 0:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            Base.metadata.create_all(bind=engine)
            print("✅ Database connected")
            return
        except OperationalError as e:
            retries -= 1
            print("⏳ Waiting for database...", e)
            time.sleep(3)

    raise Exception("❌ Database not ready")

app.include_router(router)

@app.get("/")
def health():
    return {"status": "Auth Service Running"}
