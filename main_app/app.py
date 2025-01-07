from fastapi import FastAPI, UploadFile, HTTPException
from db import connect_to_db
import requests

app = FastAPI()

# Define the URLs for the other containers (adjust if necessary)
PREPROCESSING_URL = "http://preprocessing:5001/process"
CLASSIFICATION_URL = "http://classification:5002/classify"
STOP_DETECTION_URL = "http://stop_detection:5003/detect"

# PREPROCESSING_URL = "http://localhost:5001/process"
# CLASSIFICATION_URL = "http://localhost:5002/classify"
# STOP_DETECTION_URL = "http://localhost:5003/detect"


@app.post("/upload")
async def upload_file(file: UploadFile):
    with connect_to_db() as conn:
        try:
            cur = conn.cursor()
            insert_query = """
            INSERT INTO processed_data (data)
            VALUES
                ('Sample data 1'),
                ('Sample data 2'),
                ('Sample data 3'),
                ('Sample data 4'),
                ('Sample data 5');
            """
            cur.execute(insert_query)
            conn.commit()
            # Step 1: Forward the file to the preprocessing container
            files = {"file": (file.filename, await file.read())}
            response = requests.post(PREPROCESSING_URL, files=files)

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail="Preprocessing failed"
                )

            # Step 2: Trigger classification
            response = requests.post(CLASSIFICATION_URL)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail="Classification failed"
                )

            # Step 3: Trigger stop detection
            response = requests.post(STOP_DETECTION_URL)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail="Stop detection failed"
                )

            return {
                "message": "File uploaded, preprocessing, classification, and stop detection triggered successfully"
            }

        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
