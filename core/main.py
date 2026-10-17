import random

from fastapi import FastAPI, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse

app = FastAPI()

names_list = [
    {"id": 1, "name": "ali"},
    {"id": 2, "name": "maryam"},
    {"id": 3, "name": "arousha"},
    {"id": 4, "name": "aziz"},
    {"id": 5, "name": "zahra"},
]

# /names (GET(RETRIEVE), POST(CREATE))
# /names/{id} (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)


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
def create_names(name: str):
    name_obj = {"id": random.randint(6, 100), "name": name}
    names_list.append(name_obj)
    return name_obj


@app.put("/names/{name_id}", status_code=status.HTTP_200_OK)
def update_name_detail(name_id: int, name: str):
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
