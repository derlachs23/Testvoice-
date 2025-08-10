import os
import soundfile as sf
import numpy as np
from TTS.api import TTS

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

        # Initialisiere das TTS-Modell
        # Das Modell wird beim ersten Mal heruntergeladen und zwischengespeichert.
        print("Initialisiere das TTS-Modell...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        
        print("Klone die Stimme und generiere die Sprache...")
        # Führe die Stimmklonung und Sprachsynthese durch
        tts.tts_to_file(
            text=text,
            speaker_wav=reference_wav_path,
            language="de",  # Sprache auf Deutsch gesetzt
            file_path=output_wav_path,
        )
        print(f"Sprachausgabe erfolgreich gespeichert unter: {output_wav_path}")
        return output_wav_path

    except Exception as e:
        error_message = f"Ein unerwarteter Fehler ist aufgetreten: {e}"
        print(error_message)
        return error_message

if __name__ == '__main__':
    # Beispiel für die direkte Ausführung des Skripts
    TEXT_TO_SPEAK = "Hallo, das ist ein Test, um zu sehen, wie gut diese Stimme geklont werden kann."
    REFERENCE_AUDIO = "reference_audio.wav"
    OUTPUT_AUDIO = "output_german_cloned.wav"
    
    clone_voice(TEXT_TO_SPEAK, REFERENCE_AUDIO, OUTPUT_AUDIO)
