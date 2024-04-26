from pydub import AudioSegment


def decrease_pitch(audio_file_path, output_file_path, semitones):
    sound = AudioSegment.from_file(audio_file_path)
    sound = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * (2.0 ** (semitones / 12.0)))})
    accelerated_audio = sound.speedup(playback_speed=1.2)
    accelerated_audio.export(output_file_path, format="ogg")


if __name__ == "__main__":
    decrease_pitch("input.ogg", "output.ogg", -2)
