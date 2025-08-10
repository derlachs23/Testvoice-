import pytest
import os
import soundfile as sf
from unittest.mock import patch, MagicMock

# Fügt das Projektverzeichnis zum Python-Pfad hinzu, um Importe zu ermöglichen
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clone_voice import clone_voice
from gui import voice_cloning_interface

@pytest.fixture
def temp_dir(tmp_path):
    """Erstellt ein temporäres Verzeichnis für Test-Artefakte."""
    return tmp_path

def test_clone_voice_reference_not_found():
    """
    Testet, ob clone_voice eine Fehlermeldung zurückgibt, wenn die Referenzdatei nicht existiert.
    """
    result = clone_voice("test", "non_existent_file.wav", "output.wav")
    assert "Fehler: Referenz-Audiodatei nicht gefunden" in result

@patch('clone_voice.TTS')
def test_clone_voice_success(mock_tts, temp_dir):
    """
    Testet den Erfolgsfall von clone_voice durch Mocking der TTS-Bibliothek.
    """
    mock_tts_instance = MagicMock()
    mock_tts.return_value = mock_tts_instance

    ref_file = temp_dir / "reference.wav"
    ref_file.touch() # Leere Datei erstellen
    output_file = temp_dir / "output.wav"

    result = clone_voice("hallo welt", str(ref_file), str(output_file))

    mock_tts.assert_called_once_with("tts_models/multilingual/multi-dataset/xtts_v2")
    mock_tts_instance.tts_to_file.assert_called_once_with(
        text="hallo welt",
        speaker_wav=str(ref_file),
        language="de",
        file_path=str(output_file)
    )
    assert result == str(output_file)

@patch('clone_voice.TTS')
def test_clone_voice_exception(mock_tts, temp_dir):
    """
    Testet das Verhalten von clone_voice, wenn die TTS-Bibliothek eine Ausnahme auslöst.
    """
    mock_tts.side_effect = Exception("TTS Engine failed")

    ref_file = temp_dir / "reference.wav"
    ref_file.touch()
    output_file = temp_dir / "output.wav"

    result = clone_voice("test", str(ref_file), str(output_file))
    assert "Ein unerwarteter Fehler ist aufgetreten: TTS Engine failed" in result

def test_voice_cloning_interface_no_text():
    """
    Testet die GUI-Funktion, wenn kein Text eingegeben wird.
    """
    # Die Funktion ist ein Generator, also müssen wir ihn konsumieren.
    gen = voice_cloning_interface(None, "dummy_audio.wav")
    result_path, status_message = next(gen)
    assert result_path is None
    assert "Fehler: Bitte geben Sie einen Text ein." in status_message

    gen = voice_cloning_interface("  ", "dummy_audio.wav")
    result_path, status_message = next(gen)
    assert result_path is None
    assert "Fehler: Bitte geben Sie einen Text ein." in status_message

def test_voice_cloning_interface_no_audio():
    """
    Testet die GUI-Funktion, wenn keine Audiodatei hochgeladen wird.
    """
    gen = voice_cloning_interface("test text", None)
    result_path, status_message = next(gen)
    assert result_path is None
    assert "Bitte laden Sie eine Referenz-Audiodatei hoch" in status_message

@patch('gui.clone_voice')
@patch('os.path.exists')
def test_voice_cloning_interface_success(mock_exists, mock_clone_voice, temp_dir):
    """
    Testet den Erfolgsfall der GUI-Funktion.
    """
    ref_audio_path = temp_dir / "ref.wav"
    ref_audio_path.touch()
    
    output_filename = "ref_cloned.wav"
    expected_output_path = os.path.join("cloned_voices", output_filename)

    mock_clone_voice.return_value = expected_output_path
    mock_exists.return_value = True

    gen = voice_cloning_interface("test text", str(ref_audio_path))

    # Erstes yield: "wird gestartet"
    result_path, status_message = next(gen)
    assert result_path is None
    assert "Klon-Vorgang wird gestartet" in status_message

    # Zweites yield: "erfolgreich geklont"
    result_path, status_message = next(gen)
    assert result_path == expected_output_path
    assert "Stimme erfolgreich geklont!" in status_message

    mock_clone_voice.assert_called_once_with("test text", str(ref_audio_path), expected_output_path)

@patch('gui.clone_voice')
@patch('os.path.exists')
def test_voice_cloning_interface_failure(mock_exists, mock_clone_voice, temp_dir):
    """
    Testet den Fehlerfall der GUI-Funktion.
    """
    ref_audio_path = temp_dir / "ref.wav"
    ref_audio_path.touch()
    
    error_message = "Klonen fehlgeschlagen"
    mock_clone_voice.side_effect = RuntimeError(error_message)
    mock_exists.return_value = False # Simuliert, dass die Ausgabedatei nicht erstellt wurde

    gen = voice_cloning_interface("test text", str(ref_audio_path))

    # Erstes yield ignorieren
    next(gen)

    # Zweites yield prüfen
    result_path, status_message = next(gen)
    assert result_path is None
    assert f"Ein Fehler ist aufgetreten: {error_message}" in status_message


@pytest.mark.slow
def test_clone_voice_integration_produces_valid_audio(temp_dir):
    """
    Integrationstest: Führt den echten Klon-Prozess aus und validiert die Ausgabe.
    Dieser Test ist langsam, da er das TTS-Modell lädt.
    Voraussetzung: Eine Referenzdatei existiert unter 'tests/assets/sample_ref.wav'.
    """
    # Pfade definieren
    reference_audio = "tests/assets/sample_ref.wav"
    output_audio = temp_dir / "integration_test_output.wav"
    test_text = "Dies ist ein Integrationstest."

    # Sicherstellen, dass die Referenzdatei existiert, bevor der Test läuft
    if not os.path.exists(reference_audio):
        pytest.skip("Referenz-Audiodatei 'tests/assets/sample_ref.wav' nicht gefunden. Test wird übersprungen.")

    # Die echte Funktion ohne Mocking aufrufen
    result_path = clone_voice(test_text, reference_audio, str(output_audio))

    # 1. Überprüfen, ob der Pfad korrekt zurückgegeben wurde und die Datei existiert
    assert result_path == str(output_audio)
    assert os.path.exists(result_path)

    # 2. Die Audiodatei einlesen und validieren
    audio_data, samplerate = sf.read(result_path)
    assert samplerate > 0
    assert audio_data.size > 0  # Sicherstellen, dass die Datei nicht leer ist
    assert (len(audio_data) / samplerate) > 0.1 # Sicherstellen, dass die Audiodatei eine plausible Länge hat (z.B. > 0.1s)
