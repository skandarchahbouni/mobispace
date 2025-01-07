from fastapi import FastAPI
from db import connect_to_db
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.post("/classify")
async def classify():
    with connect_to_db() as conn:
        # Handle classification logic
        logging.info("classification ...")
        pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5002)
