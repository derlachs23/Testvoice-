import os
import soundfile as sf
import numpy as np
from TTS.api import TTS
import tempfile

def clone_voice(text, reference_wav_path, output_wav_path):
    """
    Klont eine Stimme von einer Referenz-Audiodatei und generiert Sprache für den gegebenen Text.

    Args:
        text (str): Der Text, der gesprochen werden soll.
        reference_wav_path (str): Der Pfad zur Referenz-Audiodatei (.wav).
        output_wav_path (str): Der Pfad zum Speichern der generierten Audiodatei.

    Returns:
        str: Der Pfad zur generierten Audiodatei oder eine Fehlermeldung.
    """
    try:
        if not os.path.exists(reference_wav_path):
            return f"Fehler: Referenz-Audiodatei nicht gefunden unter {reference_wav_path}"

        # Load and normalize the reference audio
        audio_data, samplerate = sf.read(reference_wav_path)
        # Normalize audio to -1 to 1 range
        if audio_data.dtype == 'float32' or audio_data.dtype == 'float64':
            # Already float, just normalize
            max_val = np.max(np.abs(audio_data))
            if max_val > 0:
                normalized_audio_data = audio_data / max_val
            else:
                normalized_audio_data = audio_data # Avoid division by zero
        else:
            # Convert to float and normalize
            normalized_audio_data = audio_data.astype(np.float32)
            max_val = np.iinfo(audio_data.dtype).max
            if max_val > 0:
                normalized_audio_data = normalized_audio_data / max_val
            else:
                normalized_audio_data = normalized_audio_data # Should not happen for int types

        # Create a temporary file for the normalized audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio_file:
            temp_reference_wav_path = tmp_audio_file.name
            sf.write(temp_reference_wav_path, normalized_audio_data, samplerate)

        # Initialisiere das TTS-Modell
        print("Initialisiere das TTS-Modell...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        
        print("Klone die Stimme und generiere die Sprache...")
        # Führe die Stimmklonung und Sprachsynthese durch
        tts.tts_to_file(
            text=text,
            speaker_wav=temp_reference_wav_path, # Use the temporary normalized audio
            language="de",  # Sprache auf Deutsch gesetzt
            file_path=output_wav_path,
        )
        print(f"Sprachausgabe erfolgreich gespeichert unter: {output_wav_path}")
        return output_wav_path

    except Exception as e:
        error_message = f"Ein unerwarteter Fehler ist aufgetreten: {e}"
        print(error_message)
        return error_message
    finally:
        # Clean up the temporary file
        if 'temp_reference_wav_path' in locals() and os.path.exists(temp_reference_wav_path):
            os.remove(temp_reference_wav_path)

if __name__ == '__main__':
    # Beispiel für die direkte Ausführung des Skripts
    TEXT_TO_SPEAK = "Hallo, das ist ein Test, um zu sehen, wie gut diese Stimme geklont werden kann."
    REFERENCE_AUDIO = "reference_audio.wav"
    OUTPUT_AUDIO = "output_german_cloned.wav"
    
    clone_voice(TEXT_TO_SPEAK, REFERENCE_AUDIO, OUTPUT_AUDIO)
