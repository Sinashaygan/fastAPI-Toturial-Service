from contextlib import asynccontextmanager
from typing import Annotated, List

from fastapi import Depends, FastAPI, File, HTTPException, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Person
from schemas import PersonCreateSchema, PersonResponseSchema, PersonUpdateSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Application startup")
    yield
    print("Application shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/names", response_model=List[PersonResponseSchema])
def retrieve_names_list(
    q: str | None = Query(alias="search", title="search", description="it will searched with the title you provide", example="sina", default=None, max_length=50, deprecated=True),
    db: Session = Depends(get_db),
):
    query = db.query(Person)
    if q:
        query = query.filter(Person.name == q)
    return query.all()


@app.get("/names/{name_id}", response_model=PersonResponseSchema)
def retrieve_name_detail(name_id: int = Path(title="Object id", description="the id of the name in name_list"), db: Session = Depends(get_db)):
    person = db.get(Person, name_id)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    return person


@app.post("/names", status_code=status.HTTP_201_CREATED, response_model=PersonResponseSchema)
def create_names(person: PersonCreateSchema, db: Session = Depends(get_db)):
    person_obj = Person(name=person.name)
    db.add(person_obj)
    db.commit()
    db.refresh(person_obj)
    return person_obj


@app.put("/names/{name_id}", status_code=status.HTTP_200_OK, response_model=PersonResponseSchema)
def update_name_detail(person: PersonUpdateSchema, name_id: int = Path(), db: Session = Depends(get_db)):
    person_obj = db.get(Person, name_id)
    if person_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    person_obj.name = person.name
    db.commit()
    db.refresh(person_obj)
    return person_obj


@app.delete("/names/{name_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_name_detail(name_id: int, db: Session = Depends(get_db)):
    person = db.get(Person, name_id)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    db.delete(person)
    db.commit()


@app.get("/")
def root():
    return JSONResponse(content={"message": " Hello World!"}, status_code=status.HTTP_202_ACCEPTED)


@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {"file_name": file.filename, "content_type": file.content_type, "file_size": len(content)}


@app.post("/upload_multiple/")
async def upload_multiple(files: Annotated[List[UploadFile], File(description="چندین فایل را انتخاب کنید")]):
    return [{"file_name": file.filename, "content_type": file.content_type} for file in files]
