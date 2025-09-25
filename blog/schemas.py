from pydantic import BaseModel, EmailStr

class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(Blog):
    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    name: str
    email: EmailStr
    class Config():
        orm_mode = True
