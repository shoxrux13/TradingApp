from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
app = FastAPI(
    title="Trading App",
)

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, Request, exc: ValidationError):
    return JSONResponse(
        status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )



fake_users =[
    {"id": "1", "role": "admin", "name": "John Doe"},
    {"id": "2", "role": "investor", "name": "Jo Black"},
    {"id": "3", "role": "trader", "name": "Alice"},
    {"id": "4", "role": "investor", "name": "Bob", "degree":[
        {"id": "1", "created_at": "2021-10-10", "type_degree": "master"},
    ]},
]

class DegreeType(Enum):
   newbie = "newbie"
   master = "master"


class Degree(BaseModel):
    id: int
    created_at: str
    type_degree: str


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] =[]




@app.get("/users/{user_id}", response_model=List[User])
async def get_user(user_id: str):
    # Find the user
    user = next((user for user in fake_users if user["id"] == user_id), None)
    
    # If user is found, return a list with the user
    if user:
        return [user]
    
    # If user is not found, raise an HTTP 404 error
    raise HTTPException(status_code=404, detail="User not found")

fake_trades = [
    {"id": "1", "user_id": "1", "currency": "BTC", "side": "buy", "price": 100.0, "amount": 1.0},
    {"id": "2", "user_id": "1", "currency": "TON", "side": "sell", "price": 2000.0 , "amount": 2.0},
    {"id": "3", "user_id": "2", "currency": "BTC", "side": "buy", "price": 100.0 , "amount": 1.0},
    {"id": "4", "user_id": "2", "currency": "NOT", "side": "sell", "price": 2000.0 , "amount": 2.0},
]

@app.get("/trades")
async def get_trades(limit: int , offset: int):
    return fake_trades[offset:][:limit]


fake_users2 =[
    {"id": "1", "role": "admin", "name": "John Doe"},
    {"id": "2", "role": "investor", "name": "Jo Black"},
    {"id": "3", "role": "trader", "name": "Alice"},
]



@app.post("/users/{user_id}")
async def create_user_name(user_id: str, new_name: str):
    current_user = list(filter(lambda user: user["id"] == user_id, fake_users2))[0]
    if current_user:
        current_user["name"] = new_name
        data ={
            "message": "success",
            "code": "200",
            "data":{
                "id": current_user["id"],
                "role": current_user["role"],
                "name": current_user["name"]
            }
        }
        return data
    return {"message": "User not found"}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0.0)
    amount: float


@app.post("/trades")
async def add_trade(trades: list[Trade]):
    fake_trades.extend(trades)
    response = {
        "message": "success",
        "code": "200",
        "data": fake_trades
    }
    return response
