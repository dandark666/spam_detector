from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json
from .models import spam_predictor

@require_GET
def api_status(request):
    """Verificar estado de la API"""
    return JsonResponse({
        'status': 'active',
        'message': 'API de detección de spam - Regresión Logística',
        'model_loaded': spam_predictor.loaded,
        'model': 'logistic_regression'
    })

@require_GET
def get_metrics(request):
    """Obtener métricas del modelo"""
    try:
        metrics = spam_predictor.get_metrics()
        
        formatted_metrics = {
            'accuracy': round(metrics.get('accuracy', 0) * 100, 2),
            'precision': round(metrics.get('precision', 0) * 100, 2),
            'recall': round(metrics.get('recall', 0) * 100, 2),
            'f1_score': round(metrics.get('f1_score', 0) * 100, 2),
            'confusion_matrix': metrics.get('confusion_matrix', [[0, 0], [0, 0]]),
            'test_size': metrics.get('test_size', 0),
            'train_size': metrics.get('train_size', 0)
        }
        
        return JsonResponse({
            'status': 'success',
            'model': 'logistic_regression',
            'metrics': formatted_metrics
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_POST
@csrf_exempt
def predict_spam(request):
    """Predecir si un email es spam"""
    try:
        data = json.loads(request.body)
        email_text = data.get('email', '')
        
        if not email_text:
            return JsonResponse({
                'status': 'error',
                'message': 'No se proporcionó texto de email'
            }, status=400)
        
        result = spam_predictor.predict(email_text)
        
        return JsonResponse({
            'status': 'success',
            'model': 'logistic_regression',
            'data': result
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error en la predicción: {str(e)}'
        }, status=500)
