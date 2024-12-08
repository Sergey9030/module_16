from fastapi import FastAPI, Path, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List
from fastapi.templating import Jinja2Templates

#  python -m uvicorn module_16_5:app

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

templates = Jinja2Templates(directory="templates")


users = []


class User(BaseModel):
    id: int
    username: str = Field(min_length=1, max_length=20, description="Enter username")
    age: int = Field(ge=1, le=120, description="Enter age")


@app.get("/", response_model=List[User])  # Весь список users
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/{user_id}", response_model=List[User])  # Пользователь по ключу user_id
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    for u in users:
        if u.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": u})
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/{username}/{age}", response_model=User)  # Добавляем пользователя
async def post_user(username: str, age: int) -> User:

    if len(users) == 0:
        new_index = 1
    else:
        new_index = (users[len(users)-1].id+1)
    usr = User(id=new_index, username=username, age=age)
    users.append(usr)
    return users[len(users)-1]



@app.put("/user/{user_id}/{username}/{age}")  # Обновляем пользователя по id
async def put_user(user_id: str, username: str, age: int) -> User:
    for usr in users:
        if usr.id == int(user_id):
            usr.username = username
            usr.age = age
            return usr
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")  # Удаляем пользователя по id
async def put_user(user_id: str) -> User:
    for i in range(len(users)-1):
        if users[i].id == int(user_id):
            usr = users[i]
            users.pop(i)
            return usr
    raise HTTPException(status_code=404, detail="User was not found")
