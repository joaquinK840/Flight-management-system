from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.avl_routes import router

cors_origins = [
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
