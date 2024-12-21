from fastapi import FastAPI
from pydantic import BaseModel
from enum  import Enum
from datetime import datetime

app = FastAPI()

class Gender(bool, Enum):
   MALE: "male" # type: ignore
   FEMALE: "female" # type: ignore


class PrimaryModel(BaseModel):
    created_at: datetime
    updated_at: datetime

class NIC(BaseModel):
    nic_number: str
    nic_expiry: str
    nic_name: str


class UserAccount(BaseModel):
    account_title: str
    account_number: str
    is_active: bool
    is_dormant: bool
    is_biometric: bool
    nic: NIC


class User(PrimaryModel):
    first_name: str
    last_name: str
    phone_number: int
    email: str
    gender: Gender
    account: UserAccount


