# src/main.py
import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from src.cors import add_cors_middleware
from src.database import Base, engine
from src.routes import router

app = FastAPI(
    title="Dentist Appointment API",
    description="API to manage appointments between patients and dentists",
    version="0.1.0",
)

add_cors_middleware(app)

app.include_router(router)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown():
    pass


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
