from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


 
class PostBase(BaseModel):
    title: str
    content : str
    published : bool = True   


class UserCreate(BaseModel):
    email : EmailStr
    password :str  

class UserOut(BaseModel):
    id: int
    email : EmailStr  
    created_at: datetime
    class Config:
        orm_mode = True    

class UserLogin(BaseModel):
    email: EmailStr
    password : str     

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at: datetime
    owner_id : int
    owner : UserOut # this will automaticaly find the relationshi[ between the tables user and post]
                   #because when we get a post post we want to know the user details of the post by whom it was created
    #below code is added because while sending repsonse post response is rexpecting a dictionary for pydantic
    #but our repsonse is a sql alchemy model hence adding the below code tells it to convert sql aichemy model to
    #pydantic model
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : Post
    votes : int        



class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[int] = None   

class Vote(BaseModel):
    post_id  : int
    dir : conint(le=1)      



   