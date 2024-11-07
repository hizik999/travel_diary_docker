# schema.py
from pydantic import BaseModel, Field, constr
from typing import Optional

class Label(BaseModel):
    id: int = Field(..., ge=0, le=8, description="Label ID")  # Ограничение на диапазон ID от 0 до 8
    name: str = Field(..., max_length=25, description="Label name")

    class Config:
        orm_mode = True  # Позволяет работать с объектами SQLAlchemy напрямую

class Motion(BaseModel):
    time: int = Field(..., description="Unix timestamp", ge=0)
    user_imei: str = Field(..., description="User IMEI")
    acceleration_x: Optional[float] = None
    acceleration_y: Optional[float] = None
    acceleration_z: Optional[float] = None
    gyro_x: Optional[float] = None
    gyro_y: Optional[float] = None
    gyro_z: Optional[float] = None
    magnetometer_x: Optional[float] = None
    magnetometer_y: Optional[float] = None
    magnetometer_z: Optional[float] = None
    pressure: Optional[float] = None
    label_id: Optional[int] = Field(default=None, description="Label ID value from 0 to 8", ge=0, le=8)

    class Config:
        allow_mutation = False  # Поля неизменяемы, кроме label_id
        orm_mode = True

    def set_label_id(self, value: int):
        if not 0 <= value <= 8:
            raise ValueError("Label ID value must be between 0 and 8")
        object.__setattr__(self, 'label_id', value)
