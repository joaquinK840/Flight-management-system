from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.avl_routes import router

cors_origins = [
    "http://localhost:5173",
]

app = FastAPI()

<<<<<<< HEAD
app.include_router(router)
=======
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
>>>>>>> 645fce04a63bcbafd9232b07b4dc17f06ce271b1
