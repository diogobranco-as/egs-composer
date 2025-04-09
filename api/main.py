from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.ProductRouter import ProductRouter
from routers.PurchasedRouter import PurchasedRouter
from middleware.AuthMiddleware import get_current_user 
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title = "playerxpress-api",
    version = "1.0.",
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ProductRouter)
app.include_router(PurchasedRouter)

@app.get("/")
async def root():
    return {"message": "Welcome to PlayerXpress API!"}