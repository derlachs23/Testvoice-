# .gitpod.Dockerfile

FROM gitpod/workspace-full:latest

# Installiere Systemabhängigkeiten, die für Audioverarbeitung oder spezifische Python-Pakete benötigt werden könnten
# Beispiel: apt-get update && apt-get install -y libsndfile1

# Setze das Arbeitsverzeichnis
WORKDIR /workspace

# Kopiere requirements.txt, falls Sie eine verwenden möchten
# COPY requirements.txt .

# Führen Sie hier keine pip install Befehle aus, da dies im .gitpod.yml init-Skript besser gehandhabt wird