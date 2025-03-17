from tokenize import String

from sqlalchemy import Integer
from sqlalchemy import Column, ForeignKey

from models.db import Base, SessionLocal


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    notes = Column(Integer, ForeignKey('notes.id'), nullable=False)
    instruments = Column(Integer, ForeignKey('instruments.id'), nullable=False)

    @staticmethod
    def create(name, notes, instrument) -> int:
        db = SessionLocal()
        try:
            track = Track(name=name, notes=notes, instruments=instrument)
            db.add(track)
            db.commit()
            db.refresh(track)
            return track.id
        finally:
            db.close()


    @staticmethod
    def get(id) -> 'Track':
        db = SessionLocal()
        try:
            return db.query(Track).filter(Track.id == id).first()
        finally:
            db.close()

    @staticmethod
    def update(id, **kwargs):
        db = SessionLocal()
        try:
            track = db.query(Track).filter(Track.id == id).first()
            if track:
                for key, value in kwargs.items():
                    setattr(track, key, value)
                db.commit()
        finally:
            db.close()

    @staticmethod
    def delete(id):
        db = SessionLocal()
        try:
            track = db.query(Track).filter(Track.id == id).first()
            if track:
                db.delete(track)
                db.commit()
        finally:
            db.close()

    def __repr__(self):
        return f"Track(id={self.id}, name={self.name}, notes={self.notes})"

    def __str__(self):
        return f"Track(id={self.id}, name={self.name}, notes={self.notes})"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.id > other.id