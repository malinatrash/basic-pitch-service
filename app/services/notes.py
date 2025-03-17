from fastapi import HTTPException

from models.notes import Notes


class NoteService:
    def __init__(self):
        pass

    @staticmethod
    def get_notes_by_id(self, id) -> Notes:
        response = Notes.get(id)
        return response
