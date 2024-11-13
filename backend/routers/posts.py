from http import HTTPStatus
from backend.database  import post_table, comment_table, database
from fastapi import APIRouter, HTTPException

from backend.models.post import UserPost, UserPostIn, Comment, CommentIn, UserPostWithComments

router = APIRouter()


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query) ## first record that matches the query

## ----------------- POSTS ----------------- ##
@router.post("/posts", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    query = post_table.insert().values(**data)
    post_id = await database.execute(query)
    return {**data, "id": post_id}

@router.get("/posts/{post_id}", response_model=UserPost, status_code=200)
async def read_post(post_id: int):
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")
    return post

@router.get("/posts", response_model=list[UserPost], status_code=200)
async def get_all_posts():
    query = post_table.select()
    return await database.fetch_all(query)


@router.get("/posts/{post_id}/comments", response_model=list[Comment], status_code=200)
async def get_comments_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/posts/{post_id}/with-comments", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")
    return {
        "post": post,
        "comments": await get_comments_on_post(post_id)
    }


## ----------------- COMMENTS ----------------- ##

@router.post("/comments", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")
    data = comment.model_dump()
    query = comment_table.insert().values(**data)
    comment_id = await database.execute(query)
    return {**data, "id": comment_id}





