from fastapi import FastAPI , status , Response , HTTPException , Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import time 
from . import models
from .database import engine , get_db 
from sqlalchemy.orm import Session
from sqlalchemy import update

from psycopg2.extras import RealDictCursor  #  allows the query results to be returned as Python dictionaries instead of the default tuples

models.Base.metadata.create_all(bind=engine) # when we run our code, it create table in out database (if not there)

app = FastAPI()                   # creating instance of fast api 

# creating a schema
class Post(BaseModel):
    title : str
    content : str
    published : bool = True         # user send nothing , we have default as True , no error 
    rating : Optional[int] = None   # optional , user need to provide int else we store None in it 

all_posts = [{"title":"title of the post","content":"content of the post","id":1}]    

# try until we connect to database
while True:
     try:
        conn = psycopg2.connect(host = "localhost",port="5433",database="python_flask",user="postgres",password="123456",cursor_factory=RealDictCursor)
        cursor = conn.cursor() # we use it execute aql query
        print("database connection successful")
        break
       
     except Exception as error:
        print("failed to connect to the database")
        print("Error : ", error)
        # after every failed request, we wait 2 sec and then re-execute it 
        time.sleep(2)

def get_single_post(id : int):
     for post in all_posts:
            if post["id"] == id:
                 return post
            
def get_index_of_post_with_id(id : int):
     for i , post in enumerate(all_posts):
          if post["id"] == id:
               return i
          

# path operation -> just a route basically
@app.get("/")                     # decorator, helps to set route path and http method
def get_user():                   # path operation function , name here doesn't matter here
    return all_posts     # fast api covet this to json and send to the user  

@app.get("/posts")                # suppose if we gave it a path called "/", fast api pick the first one
def get_posts(db : Session = Depends(get_db)):      # we use Depends to call function, with calling by us , Session = Depends(get_db) => this helps us to create a session (connection) at the beginnin of request and close after that
    posts = db.query(models.Post).all()             # query to get all posts , db.query() -> generate sql
    return {"posts":posts}

@app.post("/posts")               # changing default status code
def create_posts(payload:Post,db: Session = Depends(get_db)):           # pydantic extract all the content from the body and validate using the schema that we have created and then provide type safting as well
    title = payload.title
    content = payload.content

    # here payload is pydantic model and it comes with a method model_dump to covert our pydantic model to dictionary
    # print(payload.model_dump())   

    # cursor.execute("""INSERT INTO posts (title , content) VALUES (%s,%s) RETURNING *""",(title,content))
    # new_post = cursor.fetchone()
    # conn.commit()                # saving data , when we insert something

    new_post =  models.Post(**payload.model_dump()) # ** is used for unpacking the dict into keyword argument (key = value)
    db.add(new_post)       # add new post to database
    db.commit()            # commit all database changes
    db.refresh(new_post)   # retrieve all output and store in new_post
    # at the time of query , we do not commit changes but we need to add 

    return {"new_post":new_post}

@app.get("/posts/{id}")
def get_single_post_using_id(id : int, response : Response , db : Session = Depends(get_db)):            # we can access parmas directly

    single_post = db.query(models.Post).filter(models.Post.id == id).first()   # first run the query

    if not single_post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post doesn't found with id : {id}")


    return single_post

@app.delete("/posts/{id}")
def delete_post(id : int, db : Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id}, doesn't exist")

    post.delete(synchronize_session=False)     # this will delete post
    db.commit()

    return {"message":"post deleted successfully"}

@app.put("/posts/{id}")
def update_post_using_id(id: int,posts:Post,db :Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id}, doesn't exist")

    # getting update error solve this
    upd = update(models.Post)
    val = upd.values(posts.model_dump()).where(models.Post.id == id)
    print(val)
    return {"message" : "post updated successfully"}
      
# A FastAPI code snippet demonstrating CRUD operations with a PostgreSQL database connection using pydantic for data validation.
      

      
