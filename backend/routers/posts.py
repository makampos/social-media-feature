from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from backend.models.post import UserPost, UserPostIn, Comment, CommentIn, UserPostWithComments

router = APIRouter()

post_table = {}

comments_table = {}

def find_post(post_id: int):
    return post_table.get(post_id)

## ----------------- POSTS ----------------- ##
@router.post("/posts", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post

@router.get("/posts/{post_id}", response_model=UserPost, status_code=200)
async def read_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")
    return post

@router.get("/posts", response_model=list[UserPost], status_code=200)
async def read_posts():
    return list(post_table.values())


@router.get("/posts/{post_id}/comments", response_model=list[Comment], status_code=200)
async def get_comments_on_post(post_id: int):
    return [
        comment for comment in comments_table.values() if comment["post_id"] == post_id
    ]


@router.get("/posts/{post_id}/with-comments", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")
    return {
        "post": post,
        "comments": await get_comments_on_post(post_id)
    }


## ----------------- COMMENTS ----------------- ##

@router.post("/comments", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")
    data = comment.model_dump()
    last_record_id = len(comments_table)
    new_comment = {**data, "id": last_record_id}
    comments_table[last_record_id] = new_comment
    return new_comment





