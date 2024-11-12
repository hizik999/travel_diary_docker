from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uvicorn import run
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi
from app.database import get_db, fUSERNAME, fPASSWORD
import app.crud as crud
import app.models as models
import secrets



app = FastAPI(docs_url=None, redoc_url=None) 
security = HTTPBasic()

# Укажите логин и пароль
USERNAME = fUSERNAME
PASSWORD = fPASSWORD

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/docs", include_in_schema=False)
async def get_documentation(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="Secure API Documentation")

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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Secure API",
        version="1.0.0",
        description="This is a secure API with protected documentation",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    run("main:app", reload=True)