from fastapi import FastAPI

app = FastAPI()


@app.get("/ranking")
async def ranking():
    return {"message": "Ranking Page"}

