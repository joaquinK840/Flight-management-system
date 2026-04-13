"""
Flight Management System Backend API.

This module initializes the FastAPI application for the Flight Management System,
configuring CORS middleware and registering all API route modules for flight operations,
tree management, versioning, and queue processing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.avl_routes import router as avl_router
from routes.flight_routes import router as flight_router
from routes.version_routes import router as version_router
from routes.queue_routes import router as queue_router

# CORS origins allowed for frontend communication
cors_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

# Initialize FastAPI application instance
app = FastAPI(
    title="Flight Management System API",
    description="API for managing flights using AVL trees and BST structures",
    version="1.0.0"
)

# Configure CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API route modules
app.include_router(avl_router)
app.include_router(flight_router)
app.include_router(version_router)
app.include_router(queue_router)
