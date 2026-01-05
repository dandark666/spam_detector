import os
import re
import joblib
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Descargar stopwords una vez
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords')

class LogisticSpamPredictor:
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.metrics = {}
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.loaded = False
    
    def load_models(self):
        """Cargar solo modelo de regresión logística"""
        try:
            # Cargar vectorizer
            self.vectorizer = joblib.load('models/vectorizer.pkl')
            print("Vectorizer cargado")
            
            # Cargar solo regresión logística
            model_path = 'models/logistic_regression_model.pkl'
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print("Modelo de Regresión Logística cargado")
            else:
                # Intentar cargar con otro nombre
                alt_paths = [
                    'models/logistic_regression.pkl',
                    'models/model.pkl'
                ]
                for path in alt_paths:
                    if os.path.exists(path):
                        self.model = joblib.load(path)
                        print(f"Modelo cargado desde {path}")
                        break
            
            # Cargar métricas
            metrics_path = 'models/metrics.pkl'
            if os.path.exists(metrics_path):
                with open(metrics_path, 'rb') as f:
                    all_metrics = pickle.load(f)
                    # Solo tomar métricas de regresión logística
                    if 'logistic_regression' in all_metrics:
                        self.metrics = all_metrics['logistic_regression']
                    else:
                        # Tomar el primer modelo disponible
                        for key, value in all_metrics.items():
                            self.metrics = value
                            print(f"Usando métricas de {key}")
                            break
                print("Métricas cargadas")
            
            self.loaded = True
            return True
            
        except Exception as e:
            print(f"Error cargando modelos: {e}")
            return False
    
    def preprocess_text(self, text):
        """Preprocesar texto"""
        if not isinstance(text, str):
            return ""
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Eliminar URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Eliminar emails
        text = re.sub(r'\S*@\S*\s?', '', text)
        
        # Eliminar caracteres especiales y números
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Eliminar espacios extra
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenización y stemming
        words = text.split()
        words = [self.stemmer.stem(word) for word in words if word not in self.stop_words]
        
        return ' '.join(words)
    
    def predict(self, email_text):
        """Predecir si un email es spam usando Regresión Logística"""
        if not self.loaded:
            if not self.load_models():
                raise Exception("No se pudieron cargar los modelos")
        
        if self.model is None:
            raise ValueError("Modelo de Regresión Logística no encontrado")
        
        # Preprocesar
        processed_text = self.preprocess_text(email_text)
        
        # Vectorizar
        text_vec = self.vectorizer.transform([processed_text])
        
        # Predecir
        prediction = self.model.predict(text_vec)[0]
        probability = self.model.predict_proba(text_vec)[0]
        
        return {
            'prediction': 'SPAM' if prediction == 1 else 'HAM',
            'is_spam': bool(prediction == 1),
            'spam_probability': float(probability[1]),
            'ham_probability': float(probability[0]),
            'confidence': float(max(probability)),
            'model_used': 'logistic_regression'
        }
    
    def get_metrics(self):
        """Obtener métricas del modelo"""
        if not self.loaded:
            self.load_models()
        return self.metrics

# Instancia global
spam_predictor = LogisticSpamPredictor()