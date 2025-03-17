from sqlalchemy import event, Column, Integer, String
from models.db import engine, Base


class Instrument(Base):
    __tablename__ = 'instruments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


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