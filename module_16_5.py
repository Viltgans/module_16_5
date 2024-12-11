from typing import Annotated
from fastapi import FastAPI, HTTPException, Request, Path
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory = 'templates')

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get("/")
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request":request, "users":users})

@app.get("/user/{user_id}")
async def users_list(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request":request, "user":users[user_id - 1]})


@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                    age: Annotated[int, Path(le=120, ge=18, description='Enter age', example='24')]) -> User:
    new_id = max(users, key=lambda x: int(x.id)).id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> str:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return f"User {user_id} has been updated"
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    for exist_id, user in enumerate(users):
        if user.id == user_id:
            users.pop(exist_id)
            return f'User {user_id} has been deleted'
    raise HTTPException(status_code=404, detail="User was not found")

## Запуск:
## 1. Переход в директорию: cd module_16/homework_16_5/
## 2. Сам запуск: uvicorn module_16_5:app --reload
