import logging

from sqlalchemy import Integer, Column, LargeBinary, JSON
from sqlalchemy.orm import declarative_base

from models.db import SessionLocal

logger = logging.getLogger(__name__)

Base = declarative_base()


class Notes(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    midi_id = Column(Integer, nullable=False)
    notes = Column(JSON, nullable=True)
    tempo = Column(Integer, nullable=True)

    @staticmethod
    def create(midi_id, notes, tempo=None):
        logger.info(f'Creating Notes with midi_id={midi_id}, tabs={notes}, tempo={tempo}')
        db = SessionLocal()
        try:
            note = Notes(midi_id=midi_id, notes=notes, tempo=tempo)
            db.add(note)
            db.commit()
            db.refresh(note)
            return note
        finally:
            db.close()

    @staticmethod
    def update(id, notes, tempo=None):
        logger.info(f'Updating Notes with id={id}, notes={notes}, tempo={tempo}')
        db = SessionLocal()
        try:
            note = db.query(Notes).filter(Notes.id == id).first()
            if note is not None:
                note.notes = notes
                note.tempo = tempo if tempo is not None else note.tempo
                db.commit()
                db.refresh(note)
                return note
            return None
        finally:
            db.close()

    @staticmethod
    def delete(id):
        logger.info(f'Deleting Notes with id={id}')
        db = SessionLocal()
        try:
            note = db.query(Notes).filter(Notes.id == id).first()
            if note is not None:
                db.delete(note)
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def get(id):
        logger.info(f'Getting Notes with id={id}')
        db = SessionLocal()
        try:
            return db.query(Notes).filter(Notes.id == id).first()
        finally:
            db.close()