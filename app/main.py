from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange

from pydantic.errors import EnumError
from starlette.status import HTTP_204_NO_CONTENT

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publiced: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "title of post 2", "content": "content of post 2", "id": 2}]


@app.get("/")
def root():
    print("In LOL")
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(payload: dict = Body(...)):
def create_posts(post: Post):
    # print(new_post.rating)
    # my_posts.append(post.dict())
    post_dict = post.dict()
    post_dict["id"] = randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/posts/latest")
def get_latest():
    post = my_posts[-1]
    return {"data": post}

@app.get("/posts/{id}")
# def get_post(id: int, response: Response):
def get_post(id: int):
    # print(id)
    post = find_post(id)
    # print(post)
    if not post:
        # response.status_code = 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exit")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} does not exit"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete post
    # find the index in the array
    # my_posts.pop(index)
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exit so can't delete it")

    my_posts.pop(index)

    return Response(status_code=HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exit so can't update it")

    # my_posts[index]["title"] = post.title
    # my_posts[index]["content"] = post.content

    post_dict = post.dict()
    post_dict["id"] = id

    my_posts[index] = post_dict
 
    return {"UpdatesPost" : my_posts[index]}