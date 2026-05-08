from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal

from routers import auth
from routers import employees
from routers import departments

from models.user import User
from utils.hashing import hash_password

app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DATABASE TABLES
Base.metadata.create_all(bind=engine)


# CREATE ADMIN
db = SessionLocal()

admin = db.query(User).filter(
    User.username == "admin"
).first()

if not admin:
    admin_user = User(
        username="admin",
        hashed_password=hash_password("admin123"),
        role="admin"
    )

    db.add(admin_user)
    db.commit()

    print("✅ Admin created")

else:
    print("ℹ️ Admin already exists")

db.close()


# ROUTERS
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(departments.router)


# HOME
@app.get("/")
def home():
    return {
        "message": "Employee Management API Running"
    }