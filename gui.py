import gradio as gr
from clone_voice import clone_voice
import os

# Verzeichnis für die Ausgabe-Audiodateien
OUTPUT_DIR = "cloned_voices"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def voice_cloning_interface(text, reference_audio):
    """
    Gradio-Interface-Funktion.
    Nimmt Text und eine Referenz-Audiodatei entgegen und gibt den Pfad zur geklonten Audiodatei zurück.
    """
    if text is None or text.strip() == "":
        return None, "Fehler: Bitte geben Sie einen Text ein."
    if reference_audio is None:
        return None, "Fehler: Bitte laden Sie eine Referenz-Audiodatei hoch."

    # Eindeutigen Namen für die Ausgabedatei generieren
    output_filename = f"{os.path.basename(reference_audio).split('.')[0]}_cloned.wav"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    print(f"Starte Klon-Prozess für Text: '{text}'")
    print(f"Referenz-Audio: {reference_audio}")
    print(f"Ausgabepfad: {output_path}")

    # Zeige eine Ladeanzeige in der GUI
    yield None, "Klon-Vorgang wird gestartet... (Modell wird initialisiert, das kann dauern)"

    result_path = clone_voice(text, reference_audio, output_path)

    if os.path.exists(result_path):
        print(f"Prozess beendet. Ergebnis: {result_path}")
        yield result_path, "Stimme erfolgreich geklont!"
    else:
        print(f"Fehler beim Klonen: {result_path}")
        yield None, f"Ein Fehler ist aufgetreten: {result_path}"

# Gradio-Oberfläche definieren
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎙️ Testvoice - Stimmenklon-Tool
    
    Geben Sie einen Text ein und laden Sie eine kurze Referenz-Audiodatei (WAV) hoch, um die Stimme zu klonen.
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(label="Text", placeholder="Geben Sie hier den zu sprechenden Text ein...")
            reference_audio_input = gr.Audio(label="Referenz-Audio (WAV-Datei)", type="filepath")
            clone_button = gr.Button("Stimme klonen", variant="primary")
        
        with gr.Column(scale=1):
            status_output = gr.Label(label="Status")
            audio_output = gr.Audio(label="Ergebnis")

    clone_button.click(
        fn=voice_cloning_interface,
        inputs=[text_input, reference_audio_input],
        outputs=[audio_output, status_output]
    )

    gr.Markdown("""
    **Hinweis:** Der erste Klon-Vorgang dauert länger, da das KI-Modell (ca. 2 GB) heruntergeladen werden muss. 
    Bitte haben Sie etwas Geduld.
    """)

if __name__ == "__main__":
    # Starte die Gradio-App
    demo.launch(server_name="0.0.0.0")
