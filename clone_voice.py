# clone_voice.py

import os
from TTS.api import TTS

# Pfad zum Speichern des Modells (wird automatisch heruntergeladen, wenn nicht vorhanden)
model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

# Initialisiere das TTS-Modell
# Dies kann beim ersten Mal etwas dauern, da das Modell heruntergeladen wird
print(f"Lade XTTS-v2 Modell '{model_name}'...")
tts = TTS(model_name=model_name, progress_bar=True, gpu=False) # gpu=True, falls GPU verfügbar und konfiguriert
print("Modell geladen.")

# --- Voice Cloning Beispiel ---
# Pfad zur Referenz-Audiodatei (muss eine kurze Sprachaufnahme sein, z.B. 6-10 Sekunden)
# Ersetzen Sie dies durch den tatsächlichen Pfad zu Ihrer Audiodatei
# Beispiel: Erstellen Sie eine Datei namens 'reference_audio.wav' in Ihrem Workspace
reference_audio_path = "./reference_audio.wav"

# Überprüfen, ob die Referenz-Audiodatei existiert
if not os.path.exists(reference_audio_path):
    print(f"Fehler: Referenz-Audiodatei '{reference_audio_path}' nicht gefunden.")
        print("Bitte legen Sie eine kurze WAV-Datei (ca. 6-10 Sekunden) mit der zu klonenden Stimme an.")
            print("Beispiel: Sie können eine Sprachaufnahme mit Ihrem Smartphone machen und hier hochladen.")
            else:
                # Text, der in der geklonten Stimme gesprochen werden soll
                    text_to_speak_german = "Hallo, dies ist ein Test der geklonten Stimme in deutscher Sprache."
                        output_path_german = "./output_german_cloned.wav"

                            print(f"Generiere Audio für: '{text_to_speak_german}' mit geklonter Stimme...")
                                tts.tts_to_file(
                                        text=text_to_speak_german,
                                                speaker_wav=reference_audio_path,
                                                        language="de", # Wichtig: Sprache auf Deutsch setzen
                                                                file_path=output_path_german
                                                                    )
                                                                        print(f"Generiertes Audio gespeichert unter: {output_path_german}")

                                                                            # --- Beispiel für Text-to-Speech ohne Klonen (Standardstimme) ---
                                                                                text_to_speak_default = "Dies ist ein Beispieltext mit der Standardstimme auf Deutsch."
                                                                                    output_path_default = "./output_german_default.wav"

                                                                                        print(f"Generiere Audio für: '{text_to_speak_default}' mit Standardstimme...")
                                                                                            tts.tts_to_file(
                                                                                                    text=text_to_speak_default,
                                                                                                            language="de",
                                                                                                                    file_path=output_path_default
                                                                                                                        )
                                                                                                                            print(f"Generiertes Audio gespeichert unter: {output_path_default}")

                                                                                                                            print("Skript beendet.")
                    text_to_speak_german = "Hallo, dies ist ein Test der geklonten Stimme in deutscher Sprache."
                        output_path_german = "./output_german_cloned.wav"

                            print(f"Generiere Audio für: '{text_to_speak_german}' mit geklonter Stimme...")
                                tts.tts_to_file(
                                        text=text_to_speak_german,
                                                speaker_wav=reference_audio_path,
                                                        language="de", # Wichtig: Sprache auf Deutsch setzen
                                                                file_path=output_path_german
                                                                    )
                                                                        print(f"Generiertes Audio gespeichert unter: {output_path_german}")

                                                                            # --- Beispiel für Text-to-Speech ohne Klonen (Standardstimme) ---
                                                                                text_to_speak_default = "Dies ist ein Beispieltext mit der Standardstimme auf Deutsch."
                                                                                    output_path_default = "./output_german_default.wav"

                                                                                        print(f"Generiere Audio für: '{text_to_speak_default}' mit Standardstimme...")
                                                                                            tts.tts_to_file(
                                                                                                    text=text_to_speak_default,
                                                                                                            language="de",
                                                                                                                    file_path=output_path_default
                                                                                                                        )
                                                                                                                            print(f"Generiertes Audio gespeichert unter: {output_path_default}")

                                                                                                                            print("Skript beendet.")