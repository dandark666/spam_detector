#!/usr/bin/env bash
echo "=== INICIANDO BUILD ==="

pip install --upgrade pip
pip install -r requirements.txt

python -c "import nltk; nltk.download('stopwords')"

# Descomprimir modelos si existen
if [ -d "compressed_models" ]; then
    echo "Descomprimiendo modelos..."
    mkdir -p models
    for file in compressed_models/*.gz; do
        if [ -f "$file" ]; then
            filename=$(basename "$file" .gz)
            echo "  -> $filename"
            gunzip -c "$file" > "models/$filename"
        fi
    done
fi

python manage.py collectstatic --noinput --clear

echo "=== BUILD COMPLETADO ==="
