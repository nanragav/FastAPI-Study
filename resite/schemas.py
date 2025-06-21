from pydantic import BaseModel, Field, field_validator
from typing import Optional

class BlogCreateRequest(BaseModel):

    title: str
    body: str

class BlogGetRequest(BaseModel):

    id: int

class BlogGetResponse(BaseModel):

    title: str
    body: str

class BlogUpdateRequest(BaseModel):

    id: int
    title: Optional[str] = None
    body: Optional[str] = None
            
    @field_validator('title', 'body', mode='before')

    def check_fields(cls, v):
        if v == '' or v == "":
            
            return None
        
        return v
    
class BlogDeleteRequest(BaseModel):

    id: int

class BlogDeleteResponse(BaseModel):

    message: str

class UserCreateRequest(BaseModel):

    name: str
    password: str

class UserCreateResponse(BaseModel):

    name: str
    id: int

class UserGetRequest(BaseModel):

    id: int

class UserGetResponse(BaseModel):

    id:int
    name:str

class UserLoginRequest(BaseModel):

    name: str
    password: str

class UserLoginResponse(BaseModel):

    token_type: str = 'bearer'
    access_token: str