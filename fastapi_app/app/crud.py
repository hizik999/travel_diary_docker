from sqlalchemy.orm import Session
from app.schemas import MotionSchema, LabelSchema
from app.models import Motion
from app.labels import Labels

### валидация через pydantic (то что в models) в аргументах фунеции, а создание экземпляра бд через sqlalchemy (то что в schemas) внутри функции

### CRUD label - доступные операции: очистить и заполнить заново labels, получить label по id, получить все labels

### очистить и заполнить заново labels из enum класса Labels
def create_labels(db: Session):
    db.query(LabelSchema).delete()
    for label in Labels:
        db.add(LabelSchema(id=label.value['id'], name=label.value['name']))
    db.commit()
    return {'msg': 'labels created successfully'}

### получить label(id, name) по id 
def get_label(db: Session, label_id: int):
    return db.query(LabelSchema).filter(LabelSchema.id == label_id).first()

### получить все labels
def get_labels(db: Session):
    return db.query(LabelSchema).all()

### CRUD motions - создать motion, получить motion по timestamp, получить все motions в интервале time_start и time_end, обновить label_id в motion по timestamp, ->
### -> получить все motions по user_imei, 

def create_motion(db: Session, motion: Motion):
    db_motion = MotionSchema(**motion.dict())
    db.add(db_motion)
    db.commit()
    db.refresh(db_motion)
    return db_motion

def get_motions(db: Session):
    return db.query(MotionSchema).all()

def update_motion_label(db: Session, motion_id: int, label_id: int):
    db_motion = db.query(MotionSchema).filter(MotionSchema.id == motion_id).first()
    db_motion.label_id = label_id
    db.commit()
    db.refresh(db_motion)
    return db_motion


# ### получить motion по times
# def get_motion(db: Session, time: int):
#     return db.query(MotionSchema).filter(MotionSchema.time == time).all()
# ### получить все motions в интервале time_start и time_end
# def get_motions(db: Session, time_start: int, time_end: int):
#     return db.query(MotionSchema).filter(MotionSchema.time >= time_start, MotionSchema.time <= time_end).all()

# ### получить все motions по user_imei
# def get_motions(db: Session, user_imei: str):
#     return db.query(MotionSchema).filter(MotionSchema.user_imei == user_imei).all()
