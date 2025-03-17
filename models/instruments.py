from sqlalchemy import event, Column, Integer, String
from models.db import engine, Base, SessionLocal


class Instrument(Base):
    __tablename__ = 'instruments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    @staticmethod
    def get_by_name(name):
        db = SessionLocal()
        try:
            return db.query(Instrument).filter(Instrument.name == name).first()
        finally:
            db.close()

    @staticmethod
    def get_by_id(id):
        db = SessionLocal()
        try:
            return db.query(Instrument).filter(Instrument.id == id).first()
        finally:
            db.close()


def insert_default_instruments(target, connection, **kwargs):
    connection.execute(
        target.insert(),
        [
            {"id": 1, "name": "electric_gutiar_clean"},
            {"id": 2, "name": "electric_guitar_gain"},
            {"id": 3, "name": "acoustic_guitar"},
            {"id": 4, "name": "bass"},
            {"id": 5, "name": "drums"},
            {"id": 6, "name": "piano"},
            {"id": 7, "name": "violin"},
            {"id": 8, "name": "saxophone"},
        ]
    )


event.listen(Instrument.__table__, "after_create", insert_default_instruments)

Base.metadata.create_all(engine)