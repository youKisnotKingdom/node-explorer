from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
from pathlib import Path
import shutil

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"files/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename, "location": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{file_name}")
async def read_file(file_name: str):
    file_location = f"files/{file_name}"
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_location)

@app.delete("/files/{file_name}")
async def delete_file(file_name: str):
    file_location = f"files/{file_name}"
    try:
        os.remove(file_location)
        return {"message": "File deleted successfully"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
