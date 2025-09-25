#from typing import Optional
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()

models.base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body) 
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No blogs found"})
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} not found"}
    return blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found!")
    blog.update(request.dict())
    db.commit()
    return {"detail": "updated successfully"}

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found!")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'detail': 'deleted successfully'}

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_pass = pwd_content.hash(request.password)
    new_user = models.User(name = request.name, email = request.email, password = hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.get('/users', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser], tags=['users'])
def show_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    if not users:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'No Users Found!'})
    return users

@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=['users'])
def show_user(id: int , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found!")
    return user

