from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def greeting():
    return {'data': 'Welcome to My Program!!'}

@app.get('/blog/{id}')
def blog_id(id: int):
    return {'id': id} 

@app.get('/docs')
def tmp():
    return {'data': 'hi there again its me'}

@app.get("/blog")
def index(limit: int, published: bool, sort: Optional[bool] = None):
    if published:
        return {'data': f'{limit} published blogs from db are here'}
    else:
        return {'data': f'{limit} blogs are here from all types!'}

class Blog(BaseModel):
    title: str
    content: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return request
