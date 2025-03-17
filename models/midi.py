import logging
from datetime import datetime

from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, create_engine

from models.db import Base, SessionLocal


logger = logging.getLogger(__name__)


class MidiFile(Base):
    __tablename__ = 'midi_files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)
    file_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def create(filename, data, path=None):
        db = SessionLocal()
        try:
            midi = MidiFile(filename=filename, data=data, file_path=path)
            db.add(midi)
            db.commit()
            return midi
        except Exception as e:
            logger.error(f"Error creating midi file: {e}")
            db.rollback()
            raise

    @staticmethod
    def get(id):
        db = SessionLocal()
        try:
            return db.query(MidiFile).filter_by(id=id).first()
        except Exception as e:
            logger.error(f"Error getting midi file: {e}")
            raise

    @staticmethod
    def update(id, **kwargs):
        db = SessionLocal()
        try:
            midi = db.query(MidiFile).filter_by(id=id).first()
            if midi:
                for key, value in kwargs.items():
                    setattr(midi, key, value)
                db.commit()
        except Exception as e:
            logger.error(f"Error updating midi file: {e}")
            db.rollback()
            raise

    @staticmethod
    def delete(id):
        db = SessionLocal()
        try:
            db.query(MidiFile).filter_by(id=id).delete()
            db.commit()
        except Exception as e:
            logger.error(f"Error deleting midi file: {e}")
            db.rollback()
            raise