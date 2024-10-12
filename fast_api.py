from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["fastapi"]
collection = db["post"]


class Post(BaseModel):
    id: Optional[str]
    title: str
    content: str
    created: Optional[str]

class PostCreate(BaseModel):
    title: str
    content: str


@app.get("/")
def read_root():
    return {"Hello": "World", "port": 8000}


@app.get("/post")
def get_all_post():
    posts = collection.find()
    return [Post(id=str(post["_id"]), title=post["title"], content=post["content"], created=str(post.get("created", ""))) for post in posts]


@app.get("/post/{post_id}")
def get_one_post(post_id):
    post = collection.find_one({"_id": ObjectId(post_id)})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(id=str(post["_id"]), title=post["title"], content=post["content"], created=str(post.get("created", "")))

@app.post("/post/create")
def create_one_post(post: PostCreate):
    if not post.title:
        raise HTTPException(status_code=404, detail="Need of title")

    new_post = {"title":post.title, "content": post.content, "created": datetime.now()}
    result = collection.insert_one(new_post)
    post = collection.find_one({"_id": result.inserted_id})
    return Post(id=str(post["_id"]), title=post["title"], content=post["content"], created=str(post.get("created", "")))


@app.put("/post/edit/{post_id}")
def edit_one_post(post_id: str, post: PostCreate):
    # encontramos el documento
    existing_post = collection.find_one({"_id": ObjectId(post_id)})

    if existing_post is None:
         raise HTTPException(status_code=404, detail="Post not found")
    # creamos el diccionario
    data_post = {"title":post.title, "content": post.content}
    # actualizamos el documento 
    collection.update_one({"_id": ObjectId(post_id)}, {"$set": data_post})
    # fetch document
    updated_post = collection.find_one({"_id": ObjectId(post_id)})
    return Post(id=str(updated_post["_id"]), title=updated_post["title"], content=updated_post["content"], created=str(updated_post.get("created", "")))


@app.delete("/post/delete/{post_id}")
def delete_one_post(post_id: str):
    # encontramos el documento
    existing_post = collection.find_one({"_id": ObjectId(post_id)})
    if existing_post is None:
         raise HTTPException(status_code=404, detail="Post not found")
    
    collection.delete_one({"_id": ObjectId(post_id)})
    return {"message": f"Post {post_id} deleted successfully"}
