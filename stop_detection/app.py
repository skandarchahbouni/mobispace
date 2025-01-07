from fastapi import FastAPI
from db import connect_to_db
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.post("/detect")
async def detect_stops():
    with connect_to_db() as conn:
        # Handle stop detection logic
        logging.info("stop detection ...")
        pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5003)
