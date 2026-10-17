from contextlib import asynccontextmanager
import random
from typing import List

from fastapi import (
    Body,
    FastAPI,
    File,
    Form,
    HTTPException,
    Path,
    Query,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")
    
app = FastAPI(lifespan=lifespan)

names_list = [
    {"id": 1, "name": "ali"},
    {"id": 2, "name": "maryam"},
    {"id": 3, "name": "arousha"},
    {"id": 4, "name": "aziz"},
    {"id": 5, "name": "zahra"},
]

# /names (GET(RETRIEVE), POST(CREATE))
# /names/{id} (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)

# @app.on_event("startup")
# async def startup_event():
#     print("shutting down the application")

# @app.on_event("startup")
# async def startup_event():
#     print("Starting the application")


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/names")
def retrieve_names_list(
    q: str | None = Query(
        alias="search",
        title="search",
        description="it will searched with the title you provide",
        example="sina",
        default=None,
        max_length=50,
        deprecated=True,
    ),
):
    if q:
        return [item for item in names_list if item["name"] == q]
    return names_list


@app.get("/names/{name_id}")
def retrieve_name_detail(
    name_id: int = Path(
        title="Object id",
        description="the id of the name in name_list",
        alias="object_id",
    ),
):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
    )


@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_names(name: str = Body(embed=True)):
    name_obj = {"id": random.randint(6, 100), "name": name}
    names_list.append(name_obj)
    return name_obj


@app.put("/names/{name_id}", status_code=status.HTTP_200_OK)
def update_name_detail(name_id: int = Path(), name: str = Form()):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
    )


@app.delete("/names/{name_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_name_detail(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return {"detail": "Object remove successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
    )


@app.get("/")
def root():
    return JSONResponse(
        content={"message": " Hello World!"}, status_code=status.HTTP_202_ACCEPTED
    )


@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    print(file.__dict__)
    return {
        "file_name": file.filename,
        "content_type": file.content_type,
        "file_size": len(content),
    }


@app.post("/upload_multiple/")
async def upload_multiple(files: list[UploadFile]):
    return [
        {
            "file_name": file.filename,
            "content_type": file.content_type,
            "file_size": file.size,
        }
        for file in files
    ]
 