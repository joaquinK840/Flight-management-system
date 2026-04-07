from fastapi import FastAPI
from routes.avl_routes import router

app = FastAPI()

app.include_router(router)