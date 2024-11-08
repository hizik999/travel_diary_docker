from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uvicorn import run
from app.database import get_db
import app.crud as crud
import app.models as models
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/hello")
async def hello():
    return JSONResponse(content={"message": "Hello, world!"})

### Label endpoints
### обновление labels
@app.post("/label/")
def create_labels(db: Session = Depends(get_db)):
    return {"message": crud.create_labels(db)}

### получение label по id
@app.get("/label/{label_id}", response_model=models.Label)
def get_label(label_id: int, db: Session = Depends(get_db)):
    db_label = crud.get_label(db=db, label_id=label_id)
    validate(db_label)
    return db_label

### получение всех labels
@app.get("/label/", response_model=list[models.Label])
def get_labels(db: Session = Depends(get_db)):
    db_label = crud.get_labels(db=db)
    validate(db_label)
    return db_label

### Motion endpoints
### создание motion
@app.post("/motion/")
def create_motion(motion: models.Motion, db: Session = Depends(get_db)):

    return crud.create_motion(db=db, motion=motion)

### получение всех motion
@app.get("/motion/")
def get_motions(db: Session = Depends(get_db)):
    db_motions = crud.get_motions(db=db)
    validate(db_motions)
    return db_motions

@app.put("/motion")
def update_motion_label(motion_id: int, label_id: int, db: Session = Depends(get_db)):
    return crud.update_motion_label(db=db, motion_id=motion_id, label_id=label_id)

### функция для валидации существования объекта
def validate(obj):
    if obj is None:
        raise HTTPException(status_code=404, detail="Object not found")


if __name__ == "__main__":
    run("main:app", reload=True)