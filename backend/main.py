from fastapi_offline import FastAPIOffline as FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

from routers import news
app.include_router(news.router)