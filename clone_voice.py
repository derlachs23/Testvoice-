# clone_voice.py

import os
import sys
from TTS.api import TTS

def clone_and_synthesize(tts_instance, reference_audio, text_to_speak, output_path, language="de"):
    """Generiert Audio mit einer geklonten Stimme."""
    print(f"Generiere Audio für: '{text_to_speak}' mit geklonter Stimme...")
    tts_instance.tts_to_file(
        text=text_to_speak,
        speaker_wav=reference_audio,
        language=language,
        file_path=output_path
    )
    print(f"Generiertes Audio gespeichert unter: {output_path}")

def synthesize_default(tts_instance, text_to_speak, output_path, language="de"):
    """Generiert Audio mit der Standardstimme."""
    print(f"Generiere Audio für: '{text_to_speak}' mit Standardstimme...")
    tts_instance.tts_to_file(
        text=text_to_speak,
        language=language,
        file_path=output_path
    )
    print(f"Generiertes Audio gespeichert unter: {output_path}")

def main():
    """Hauptfunktion zum Laden des Modells und zur Durchführung der TTS-Aufgaben."""
    # Pfad zum Speichern des Modells (wird automatisch heruntergeladen, wenn nicht vorhanden)
    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

    # Initialisiere das TTS-Modell
    # Dies kann beim ersten Mal etwas dauern, da das Modell heruntergeladen wird
    print(f"Lade XTTS-v2 Modell '{model_name}'...")
    # Setze gpu=True, falls eine kompatible GPU verfügbar und konfiguriert ist, um die Generierung zu beschleunigen.
    tts = TTS(model_name=model_name, progress_bar=True, gpu=False)
    print("Modell geladen.")

    # --- Voice Cloning Beispiel ---
    # Pfad zur Referenz-Audiodatei (muss eine kurze Sprachaufnahme sein, z.B. 6-10 Sekunden)
    # Ersetzen Sie dies durch den tatsächlichen Pfad zu Ihrer Audiodatei
    # Beispiel: Erstellen Sie eine Datei namens 'reference_audio.wav' in Ihrem Workspace
    reference_audio_path = "./reference_audio.wav"

    # Überprüfen, ob die Referenz-Audiodatei existiert
    if not os.path.exists(reference_audio_path):
        print(f"Fehler: Referenz-Audiodatei '{reference_audio_path}' nicht gefunden.", file=sys.stderr)
        print("Bitte legen Sie eine kurze WAV-Datei (ca. 6-10 Sekunden) mit der zu klonenden Stimme an.", file=sys.stderr)
        print("Beispiel: Sie können eine Sprachaufnahme mit Ihrem Smartphone machen und hier hochladen.", file=sys.stderr)
        sys.exit(1) # Beendet das Skript mit einem Fehlercode

    # Klonen und Generieren
    text_to_clone = "Hallo, dies ist ein Test der geklonten Stimme in deutscher Sprache."
    output_cloned = "./output_german_cloned.wav"
    clone_and_synthesize(tts, reference_audio_path, text_to_clone, output_cloned, language="de")

    # Generieren mit Standardstimme
    text_default = "Dies ist ein Beispieltext mit der Standardstimme auf Deutsch."
    output_default = "./output_german_default.wav"
    synthesize_default(tts, text_default, output_default, language="de")

    print("Skript beendet.")

if __name__ == "__main__":
    main()