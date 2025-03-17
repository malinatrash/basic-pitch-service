import mido

def clean_midi(midi_path, out_path, noise_threshold=20, min_duration=10):
    # Открываем старый MIDI файл
    midi = mido.MidiFile(midi_path)
    
    # Создаем новый MIDI файл
    new_midi = mido.MidiFile()
    
    for track in midi.tracks:
        new_track = mido.MidiTrack()
        new_midi.tracks.append(new_track)

        for msg in track:
            # Проверяем, является ли сообщение нотным событием
            if msg.type == 'note_on' or msg.type == 'note_off':
                # Пропускаем ноты ниже порога и ноты с короткой длительностью
                if msg.velocity >= noise_threshold:
                    # Добавляем ноту в новый трек, если она соответствует условиям
                    new_track.append(msg)

            # Добавляем остальные сообщения в новый трек
            else:
                new_track.append(msg)

    # Сохраняем новый MIDI файл
    new_midi.save(out_path)

if __name__ == '__main__':
    clean_midi('input.mid', 'output.mid', noise_threshold=64, min_duration=100)
