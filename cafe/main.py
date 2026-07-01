from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CartItem(BaseModel):
    user_id: int
    product_id: int


cart = []


@app.post("/cart/add")
def add_to_cart(item: CartItem):
    cart.append(item)
    return {"message": "Добавлено"}


def get_conn():
    return sqlite3.connect("app.db")


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_user(username: str, password: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users(username, password) VALUES(?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()


init_db()


class User(BaseModel):
    username: str
    password: str


@app.post("/register")
def register(user: User):
    add_user(user.username, user.password)
    return {"message": "Пользователь создан"}


@app.post("/login")
def login(user: User):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (user.username, user.password)
    )

    result = cur.fetchone()
    conn.close()

    if result:
        return {"ok": True}

    return {"ok": False}


#korzina

@app.get("/cart/{user_id}")
def get_cart(user_id: int):
    result = []

    for item in cart:
        if item.user_id == user_id:
            result.append({
                "id": item.product_id,
                "name": f"Товар №{item.product_id}",
                "price": 250
            })

    return result

@app.delete("/cart/remove/{product_id}")
def remove_product(product_id: int):
    global cart

    cart = [
        item for item in cart
        if item.product_id != product_id
    ]

    return {"message":"Удалено"}


