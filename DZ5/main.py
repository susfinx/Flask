import uvicorn as uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class UserOut(BaseModel):
    id: int
    name: str
    email: str


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class User(UserIn):
    id: int


users = []
for i in range(10):
    users.append(User(
        id=i + 1,
        name=f'name{i + 1}',
        email=f'email{i + 1}@mail.ru',
        password='123'
    ))


@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/registration", response_class=HTMLResponse)
async def registration_form(request: Request):
    return templates.TemplateResponse("registration_form.html", {"request": request})


@app.post("/registration")
async def registration_confirm(name=Form(), email=Form(), password=Form()):
    new_user = UserIn(name=name, email=email, password=password)
    if new_user:
        users.append(
            User(id=len(users) + 1, name=name, email=email,
                 password=password))
        return users[-1]
    raise HTTPException(status_code=404, detail="Cant create User")


@app.post("/users")
async def create_user(new_user: UserIn):
    users.append(
        User(id=len(users) + 1, name=new_user.name, email=new_user.email,
             password=new_user.password))
    return {"user": users[-1]}


@app.put("/users/", response_model=User)
async def edit_user(user_id: int, new_user: UserIn):
    for i in range(0, len(users)):
        if users[i].id == user_id:
            current_user = users[user_id - 1]
            current_user.name = new_user.name
            current_user.email = new_user.email
            current_user.password = new_user.password
            return current_user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/", response_model=dict)
async def user(user_id: int):
    for i in range(0, len(users)):
        if users[i].id == user_id:
            users.remove(users[i])
            return {"message": "User was deleted"}
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)