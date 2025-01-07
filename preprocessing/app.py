from fastapi import FastAPI
from db import connect_to_db
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.post("/process")
async def process_data():
    with connect_to_db() as conn:
        # Handle data preprocessing logic
        logging.info("preprocessing ...")
        pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5001)
