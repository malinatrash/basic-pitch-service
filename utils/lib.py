import mido

# Единственная необходимая функция для работы с MIDI файлами
def get_midi_info(midi_path) -> dict:
    """Получение информации о MIDI файле"""
    try:
        midi_file = mido.MidiFile(midi_path)
        tempo = midi_file.ticks_per_beat
        
        # Подсчет количества нот в файле
        note_count = 0
        for track in midi_file.tracks:
            for msg in track:
                if msg.type in ['note_on', 'note_off']:
                    note_count += 1
        
        return {
            "tempo": tempo,
            "note_count": note_count,
            "track_count": len(midi_file.tracks)
        }
    except Exception as e:
        return {"error": f"Ошибка при обработке MIDI файла: {str(e)}"}

