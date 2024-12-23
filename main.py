from urllib.parse import quote_plus
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum  import Enum
from datetime import datetime
from pymongo import AsyncMongoClient  # type: ignore
from bson.objectid import ObjectId # type: ignore
from typing import Optional, Dict
import bcrypt 

username = "hsBank"
password = "Pakkhi@321"

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

mongo_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@hs-bank.cqre4.mongodb.net/?retryWrites=true&w=majority&appName=hs-bank"
client = AsyncMongoClient(mongo_uri)

db = client.hsBank


app = FastAPI()


def bson_to_dict(bson_obj):
    if bson_obj:
        bson_obj["_id"] = str(bson_obj["_id"])  # Convert ObjectId to string
        return bson_obj
    return {}

class Gender(str, Enum):
   MALE = "male" # type: ignore
   FEMALE = "female" # type: ignore


class Nic_Expiry(BaseModel):
    day: str
    month: str
    year: str

class Nic_Expiry(BaseModel):
    day: str
    month: str
    year: str

class PrimaryModel(BaseModel):
    created_at: datetime
    updated_at: datetime

class NIC(BaseModel):
    nic_number: str
    nic_expiry: Nic_Expiry  
    nic_name: str


class UserAccount(BaseModel):
    account_title: str
    account_number: str
    is_active: bool 
    is_dormant: bool 
    is_biometric: bool 
    nic: NIC


class User(BaseModel):
    first_name: str
    last_name: str
    phone_number: int
    password: str
    email: str
    gender: Gender
    account: UserAccount


class UserByEmail(BaseModel):
    email: str


@app.get("/")
def root():
    return ("KING BABAR AZAM")


class UserLogin(BaseModel):
    email: str
    password: str
    
@app.post("/login")
async def login(credentials: UserLogin):
    check_email = await db.users.find_one({
        "email": credentials.email
    })
    if not check_email:
        raise HTTPException(status_code=404, detail="User with this email doesn't exists.")
    b_password = credentials.password.encode('utf-8')
    check_password = bcrypt.checkpw()

@app.post('/users')
async def create_user(user: User):
    check_email = await db.users.find_one({
        "email": user.email
    })
    print(check_email)
    if check_email:
        raise HTTPException(status_code=201, detail="User with this email already exists")
    password = user.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    
    user_dict = user.dict()
    user_dict.update({"password": hashed_password})
    
    user_insert = await db.users.insert_one(user_dict)
    return "User Created"



@app.get("/users/{id}")
async def get_user(id):
    print(id)
    user = await db.users.find_one({"_id": ObjectId(id)})
    user_dict = bson_to_dict(user)
    if(user_dict):
        return user_dict
    else: 
        raise HTTPException(status_code=404, detail="User with this id doesn't exit")


@app.get("/users/is-active/{id}")
async def is_user_active(id):
    user = await db.users.find_one({
        "_id": ObjectId(id)
    })
    user_dict = bson_to_dict(user)
    if user_dict["account"]["is_active"]:
        raise HTTPException(status_code=200, detail="This user is active")
    else:
        raise HTTPException(status_code=200, detail="This user is inactive")
    
   


@app.get("/users/nic_expiry/{id}")
async def get_nic(id):
     now = datetime.now()
     user = await db.users.find_one({
            "_id": ObjectId(id)      
     }) 
     user_dict = bson_to_dict(user)
     day = user_dict['account']['nic']['nic_expiry']['day']
     month = user_dict['account']['nic']['nic_expiry']['month']
     year = user_dict['account']['nic']['nic_expiry']['year']
     expiry_date = datetime(int(year), int(month), int(day))
     
     if expiry_date < now:
         return "Nic is expired"
     else:
         return "Nic is not expired"
             

@app.post("/users/by-email")
async def get_user_email(email: UserByEmail):
    user = await db.users.find_one({"email":email.email})
    if user:
        return bson_to_dict(user)
    else:
        raise HTTPException(status_code=404, detail= "User with this email doesn't exit")
