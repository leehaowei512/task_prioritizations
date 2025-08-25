import logging

from fastapi import FastAPI

from api_layer.endpoints import router as api_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Borrowed Beans Task API",
    version="1.0.0",
    description="API for managing tasks with optimized view-based queries",
)

# Include API routes
app.include_router(api_router, prefix="/api/v1", tags=["tasks", "teams", "allocation"])


@app.get("/")
async def root():
    return {"message": "Borrowed Beans Task Management API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
