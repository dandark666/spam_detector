#!/usr/bin/env bash
# Script de construcción para Render - VERSIÓN CORREGIDA

echo "=== INICIANDO BUILD EN RENDER ==="

# 1. Actualizar pip
pip install --upgrade pip

# 2. Instalar dependencias desde requirements.txt
echo "Instalando dependencias de requirements.txt..."
pip install -r requirements.txt

# 3. Descargar datos NLTK
echo "Descargando datos NLTK..."
python -c "import nltk; nltk.download('stopwords', quiet=True)"

# 4. Crear directorio de modelos si no existe
mkdir -p models

# 5. Descomprimir modelos si están comprimidos
echo "Verificando modelos comprimidos..."
if [ -d "compressed_models" ]; then
    echo "Descomprimiendo modelos..."
    for file in compressed_models/*.gz; do
        if [ -f "$file" ]; then
            filename=$(basename "$file" .gz)
            echo "  Descomprimiendo: $filename"
            gzip -dk "$file"
            mv "$(basename "$file" .gz)" "models/$filename" 2>/dev/null || true
        fi
    done
fi

# 6. Verificar que existen archivos de modelos
echo "Verificando modelos..."
for model_file in "models/vectorizer.pkl" "models/logistic_regression_model.pkl" "models/metrics.pkl"; do
    if [ -f "$model_file" ]; then
        size=$(ls -lh "$model_file" | awk '{print $5}')
        echo "  ✅ $model_file ($size)"
    else
        echo "  ⚠️  $model_file NO ENCONTRADO"
    fi
done

# 7. Migraciones de base de datos
echo "Aplicando migraciones de Django..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# 8. Colectar archivos estáticos
echo "Colectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "=== BUILD COMPLETADO CON ÉXITO ==="
