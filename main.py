import datetime

from typing import Annotated

from fastapi import FastAPI, Query, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class BaseLicense(BaseModel):
    type: str
    price: str


class UserLicense(BaseLicense):
    acquisition_date: datetime.date
    expiration_date: datetime.date


class User(BaseModel):
    name: str
    password: str
    mugshot: UploadFile | None = None
    age: int | None = None
    licenses: list[UserLicense] = []


users = {
    "user1": {
        "name": "john",
        "password": "haha",
        "age": "30",
        "licenses": {
            "type": "Improviser 20 Weeks",
            "price": "Your firstborn",
            "acquisition_date": "2023-09-04",
            "expiration_date": "2024-01-26"
        }
    },
    "user2": {
        "name": "doe",
        "password": "haha",
        "licenses": {
            "type": "Spotify Premium for Students 20 Years",
            "price": "Perfectly fair",
            "acquisition_date": "2004-04-26",
            "expiration_date": "2024-04-25"
        }
    }
}


@app.get("/users/", tags=["users"])
def get__all_users():
    print("obtained")
    return users


@app.get("/users/{user_id}/", response_model=User, response_model_exclude={"password"}, tags=["users"])
def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Not found")
    print("obtained")
    return users[user_id]


@app.post("/users/create/", response_model=User, response_model_exclude={"password"}, tags=["users"])
def create_user(name: Annotated[str, Query(min_length=2)], pw: Annotated[str, Query(min_length=4, max_length=16)], mugshot: UploadFile | None = None):
    user = {
        "name": name,
        "password": pw,
        "mugshot": mugshot
    }
    users["user" + str(len(users) + 1)] = user
    print("created")
    return users["user3"]


@app.put("/users/update/{user_id}/", response_model=User, response_model_exclude={"password"}, tags=["users"])
def get_user(user_id: str, user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Not found")
    # edit = {
    #     "name": name,
    #     "password": pw
    # }
    # users[user_id] = edit
    prev_user = users[user_id]
    prev_user_model = User(**prev_user)
    update_data = user.model_dump(exclude_unset=True)
    updated_user = prev_user_model.model_copy(update=update_data)
    users[user_id] = jsonable_encoder(updated_user)
    print("updated")
    return users[user_id]


@app.delete("/users/delete/{user_id}/", tags=["users"])
def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Not found")
    del users[user_id]
    print("deleted")
    return users
