from typing import Optional
from fastapi import FastAPI, Response, status , HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session 
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class New_book(BaseModel):
    id : Optional[int]
    book_title : str
    author : str
    #student_id : int
    #book_status = str

class Assiging_book(BaseModel):
    id : int
    #book_title : Optional[str]
    student_id : int
    book_status : str

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='LMS', user='postgres', password='password',
                            cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Successfully logined")
        break
    except Exception as error:
        print("login not successful")
        print("error was", error)
        time.sleep(2)


@app.get("/")
def library_data(db: Session = Depends(get_db)):
    d = db.query(models.Table).all()
    if not d:
        return (f'Database: {models.Table.__tablename__} is empty')
    return d

@app.post("/new_book",status_code=status.HTTP_201_CREATED)
def new_book(new: New_book, db: Session = Depends(get_db)):
    newentry = models.Table(**new.dict())
    db.add(newentry)
    db.commit()
    db.refresh(newentry)
    print("new book added to library")
    return {newentry}

@app.delete("/delete_book/{id}")
def delete_book(id : int,db: Session = Depends(get_db)):
    entry = db.query(models.Table).filter(models.Table.id == id)
    print(id)
    if entry.first() == None:
        print("item not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    entry.delete(synchronize_session=False)
    db.commit()
    print(f'book id: {id} deleted successfully')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/assigning_book/{id}")
def assigning_book(id : int, new_data : Assiging_book, db: Session = Depends(get_db)):
    data = db.query(models.Table).filter(models.Table.id == id)
    data1 = data.first()
    if not data1:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    data.update(new_data.dict(),synchronize_session=False)
    db.commit()
    return {"message": new_data}



    


