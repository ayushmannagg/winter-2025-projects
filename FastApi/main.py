# CRUD
# Create 
# read
# Update
# Delete

# http requests
# get
# post
# put
# delete

from fastapi import FastAPI, HTTPException, status, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

users={
    1: {
        "name":"josh",
        "website":"ww.google.com",
        "age":20,
        "role":"developer"
    }
}

# base pydantic models
class User(BaseModel):
    name:str
    website:str
    age:int
    role:str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None





#endpoint(URL)
@app.get("/")
def root():
    return{"message":"welcome to fastapi"}


# search a user
@app.get("/users/search")
def search_by_name(name: Optional[str]= None):
    if not name:
        return {"message":"name parameter is required"}
    for user in users.values():
        if user["name"] == name:
            return user
    raise HTTPException(status_code=404, detail="User Not Found")


# get users
@app.get("/users/{user_id}")
def get_user(user_id:int = Path (..., description="The ID you want to get", gt=0, lt=100)):
    if user_id not in users:
        raise HTTPException(status_code=404, detail = "User Not Found!")
    return users[user_id]



# create a user
@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def create_user(user_id:int, user:User):
    if user_id in users:
        raise HTTPException(status_code = 400, detail = "User Already Exists")

    users[user_id] = user.dict()
    return user


# update a user
@app.put("/users/{user_id}")
def update_user(user_id:int, user:UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code = 400, detail = "User is not there")
    
    current_user = users[user_id]

    if user.name is not None:
        current_user["name"] = user.name
    if user.website is not None:
        current_user["website"] = user.website
    if user.age is not None:
        current_user["age"] = user.age
    if user.role is not None:
        current_user["role"] = user.role


# delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code = 400, detail = "User is not there")
    
    deleted_user = users.pop(user_id)
    return{"message":"User has been deleted", "deleted user":deleted_user}



        