from typing import List
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query, Path, Body

from models import Gender, Role, User, UserUpdateRequest, Genre, Author, Book

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("9a0ccf81-4732-4484-a511-ef62857db029"),
        first_name="Anna",
        last_name="Farmer",
        gender=Gender.female,
        roles=[Role.student],
    ),
    User(
        id=UUID("113d9f76-1417-460d-8b06-a2f3ac2720c8"),
        first_name="John",
        last_name="Doe",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


# http://127.0.0.1:8000/book?q=qqqq
@app.get("/user")
def get_user(
    q: List[str] = Query(
        ["test", "test2"],
        min_length=2,
        max_length=10,
        description="Query",
        deprecated=True,
    )
):
    return q


@app.post('/book', response_model=Book, response_model_include={"pages", "date"})
def create_book(item: Book):
    return item


@app.post('/book')
def create_book(item: Book, author: Author, quantity: int = Body(...)):
    return {"item": item, "author": author, "quantity": quantity}


@app.post('/author')
def create_author(author: Author = Body(..., embed=True)):
    return {"author": author}


# http://127.0.0.1:8000/book/2?pages=200
@app.get('/book/{pk}')
def get_single_book(pk: int = Path(..., gt=1, le=20), pages: int = Query(None, gt=10, le=500)):
    return {"pk": pk, "pages": pages}


# http://127.0.0.1:8000/22?q=qqqqqqqq
@app.get("/{pk}")
def get_item(pk: int, q: str = None):
    return {"key": pk, "q": q}


# http://127.0.0.1:8000/user/2/items/tv/
@app.get("/user/{pk}/items/{item}/")
def get_user_item(pk: int, item: str):
    return {"user": pk, "item": item}


@app.get("/api/v1/users/")
async def fetch_users():
    return db


@app.post("/api/v1/users/")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": "User deleted"}
    return HTTPException(status_code=404, detail="User not found")


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.put("/api/v1/users/{user id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(status_code=404, detail="User not found")
