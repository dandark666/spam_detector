import os
import re
import joblib
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Descargar stopwords si no están
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
        """Cargar modelos"""
        try:
            # Cargar vectorizer
            vectorizer_path = 'models/vectorizer.pkl'
            if os.path.exists(vectorizer_path):
                self.vectorizer = joblib.load(vectorizer_path)
            else:
                print("Vectorizer no encontrado")
                return False
            
            # Cargar modelo
            model_path = 'models/logistic_regression_model.pkl'
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                print("Modelo no encontrado")
                return False
            
            # Cargar métricas
            metrics_path = 'models/metrics.pkl'
            if os.path.exists(metrics_path):
                with open(metrics_path, 'rb') as f:
                    all_metrics = pickle.load(f)
                    if 'logistic_regression' in all_metrics:
                        self.metrics = all_metrics['logistic_regression']
                    else:
                        # Tomar el primer modelo disponible
                        for key, value in all_metrics.items():
                            self.metrics = value
                            break
            
            self.loaded = True
            return True
            
        except Exception as e:
            print(f"Error cargando modelos: {e}")
            return False
    
    def preprocess_text(self, text):
        """Preprocesar texto"""
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\S*@\S*\s?', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        words = text.split()
        words = [self.stemmer.stem(word) for word in words if word not in self.stop_words]
        
        return ' '.join(words)
    
    def predict(self, email_text):
        """Predecir si un email es spam"""
        if not self.loaded:
            if not self.load_models():
                raise Exception("No se pudieron cargar los modelos")
        
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
