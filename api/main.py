from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.AuthRouter import AuthRouter
from routers.ProductRouter import ProductRouter
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

app.include_router(AuthRouter)
app.include_router(ProductRouter)

@app.get("/")
async def root():
    return {"message": "Welcome to PlayerXpress API!"}