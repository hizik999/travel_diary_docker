from sqlalchemy import Column, Float, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.database import Base

class LabelSchema(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)  # No auto-increment to restrict IDs 0-8
    name = Column(String, nullable=False)

    # Опционально: определение строкового представления для удобства отладки
    def __repr__(self):
        return f"<Label(id={self.id}, name={self.name})>"

class MotionSchema(Base):
    __tablename__ = "motions"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(BigInteger, nullable=False)
    user_imei = Column(String, nullable=False)
    acceleration_x = Column(Float, nullable=True)
    acceleration_y = Column(Float, nullable=True)
    acceleration_z = Column(Float, nullable=True)
    gyro_x = Column(Float, nullable=True)
    gyro_y = Column(Float, nullable=True)
    gyro_z = Column(Float, nullable=True)
    magnetometer_x = Column(Float, nullable=True)
    magnetometer_y = Column(Float, nullable=True)
    magnetometer_z = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    label_id = Column(Integer, ForeignKey(f'{LabelSchema.__tablename__}.id'), nullable=True)

    # Связь с моделью LabelSchema
    label = relationship("LabelSchema")

    def set_label_id(self, value: int):
        if not 0 <= value <= 8:
            raise ValueError("Label ID must be between 0 and 8")
        object.__setattr__(self, 'label_id', value)
