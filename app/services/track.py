from models.track import Track


class TrackService:

    @staticmethod
    def get_track_by_id(id):
        return Track.get(id)

    @staticmethod
    def create_track(name, notes, instrument):
        return Track.create(name, notes, instrument)