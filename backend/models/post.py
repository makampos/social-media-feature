from pydantic import BaseModel, ConfigDict  ## classes to define the model of the request body

class UserPostIn(BaseModel):
    body: str

class UserPost(UserPostIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class CommentIn(BaseModel):
    body: str
    post_id: int

class Comment(CommentIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]

