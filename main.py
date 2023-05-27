import uvicorn
from fastapi import FastAPI

from routes.ranking import router as rank_router
from routes.recommend import router as rec_router

app = FastAPI()
app.include_router(rank_router)  # 다른 route파일들을 불러와 포함시킴
app.include_router(rec_router)


@app.get("/")  # Route Path
def root():
    return {"message": "404 Not Found"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
