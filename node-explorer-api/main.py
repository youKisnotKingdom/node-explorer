from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
from pathlib import Path
import shutil
from fastapi.middleware.cors import CORSMiddleware
import mimetypes

app = FastAPI()


# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue.jsが動作しているURL
    allow_credentials=True,
    allow_methods=["*"],  # 全てのメソッドを許可
    allow_headers=["*"],  # 全てのヘッダーを許可
)

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
    
@app.get("/files/")
async def list_files():
    directory = Path("files")
    files = [f.name for f in directory.iterdir() if f.is_file()]
    return {"files": files}

import mimetypes

@app.get("/files/{file_name}/content")
async def read_file_content(file_name: str):
    file_path = f"files/{file_name}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    mime_type, _ = mimetypes.guess_type(file_path)
    try:
        if mime_type == 'application/pdf':
            return FileResponse(file_path, media_type='application/pdf')
        else:
            with open(file_path, "r") as file:
                content = file.read()
            return {"content": content, "mime_type": mime_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


