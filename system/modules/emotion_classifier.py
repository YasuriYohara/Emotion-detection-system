"""
Emotion Classifier Module
Handles emotion detection using FER and DeepFace libraries.
Implements confidence thresholding and multi-model support.
"""

import numpy as np
from typing import Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class EmotionClassifier:
    """
    Emotion classification with multiple model backends.
    """
    
    # Confidence threshold for reliable predictions
    CONFIDENCE_THRESHOLD = 0.40  # 40%
    
    # Emotion labels mapping
    EMOTION_LABELS = {
        'angry': 'Anger',
        'disgust': 'Disgust',
        'fear': 'Fear',
        'happy': 'Happiness',
        'sad': 'Sadness',
        'surprise': 'Surprise',
        'neutral': 'Neutral'
    }
    
    def __init__(self, model_type='fer'):
        """
        Initialize emotion classifier.
        
        Args:
            model_type (str): 'fer' or 'deepface'
        """
        self.model_type = model_type
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the emotion detection model."""
        try:
            if self.model_type == 'fer':
                from fer import FER
                # mtcnn=True for better face detection, but slower
                # mtcnn=False uses OpenCV for faster processing
                self.model = FER(mtcnn=False)
                print("FER model loaded successfully")
            elif self.model_type == 'deepface':
                # DeepFace is loaded on-demand per prediction
                print("DeepFace will be loaded on-demand")
            else:
                raise ValueError(f"Unknown model type: {self.model_type}")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
    
    def predict_emotion_fer(self, image: np.ndarray) -> Optional[Dict]:
        """
        Predict emotion using FER library.
        
        Args:
            image (np.ndarray): Input face image (BGR format)
            
        Returns:
            Dict with emotion predictions or None if failed
        """
        try:
            # Detect emotions
            result = self.model.detect_emotions(image)
            
            if not result or len(result) == 0:
                return None
            
            # Get first detection (primary face)
            emotions = result[0]['emotions']
            
            return emotions
        except Exception as e:
            print(f"FER prediction error: {str(e)}")
            return None
    
    def predict_emotion_deepface(self, image_path: str) -> Optional[Dict]:
        """
        Predict emotion using DeepFace library.
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            Dict with emotion predictions or None if failed
        """
        try:
            from deepface import DeepFace
            
            # Analyze emotion
            result = DeepFace.analyze(
                img_path=image_path,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            
            # Handle both single result and list of results
            if isinstance(result, list):
                result = result[0]
            
            emotions = result.get('emotion', {})
            
            # Normalize emotion names to match FER format
            normalized_emotions = {}
            for key, value in emotions.items():
                normalized_key = key.lower()
                normalized_emotions[normalized_key] = value / 100.0  # Convert to 0-1 range
            
            return normalized_emotions
        except Exception as e:
            print(f"DeepFace prediction error: {str(e)}")
            return None
    
    def classify_emotion(self, image=None, image_path=None) -> Dict:
        """
        Classify emotion with confidence scoring.
        
        Args:
            image (np.ndarray): Input image (for FER)
            image_path (str): Path to image (for DeepFace)
            
        Returns:
            Dict containing:
                - emotion (str): Predicted emotion label
                - confidence (float): Confidence score (0-100)
                - all_scores (dict): All emotion scores
                - is_confident (bool): Whether prediction meets threshold
                - error (str): Error message if any
        """
        result = {
            'emotion': None,
            'confidence': 0.0,
            'all_scores': {},
            'is_confident': False,
            'error': None
        }
        
        try:
            # Get predictions based on model type
            if self.model_type == 'fer' and image is not None:
                emotions = self.predict_emotion_fer(image)
            elif self.model_type == 'deepface' and image_path is not None:
                emotions = self.predict_emotion_deepface(image_path)
            else:
                result['error'] = "Invalid input for model type"
                return result
            
            if emotions is None or len(emotions) == 0:
                result['error'] = "No emotion detected in image"
                return result
            
            # Find dominant emotion
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])
            emotion_key, confidence = dominant_emotion
            
            # Normalize emotion label
            emotion_label = self.EMOTION_LABELS.get(emotion_key, emotion_key.capitalize())
            
            # Convert confidence to percentage
            confidence_percent = confidence * 100 if confidence <= 1.0 else confidence
            
            # Check if prediction is confident
            is_confident = confidence_percent >= (self.CONFIDENCE_THRESHOLD * 100)
            
            # Format all scores for display
            all_scores = {
                self.EMOTION_LABELS.get(k, k.capitalize()): round(v * 100, 2) if v <= 1.0 else round(v, 2)
                for k, v in emotions.items()
            }
            
            result['emotion'] = emotion_label
            result['confidence'] = round(confidence_percent, 2)
            result['all_scores'] = all_scores
            result['is_confident'] = is_confident
            
        except Exception as e:
            result['error'] = f"Classification error: {str(e)}"
        
        return result
    
    def get_emotion_emoji(self, emotion: str) -> str:
        """
        Get emoji representation for emotion.
        
        Args:
            emotion (str): Emotion label
            
        Returns:
            str: Emoji character
        """
        emoji_map = {
            'Happiness': '😊',
            'Sadness': '😢',
            'Anger': '😠',
            'Fear': '😨',
            'Surprise': '😲',
            'Disgust': '🤢',
            'Neutral': '😐'
        }
        return emoji_map.get(emotion, '😐')
    
    def get_confidence_level(self, confidence: float) -> str:
        """
        Get descriptive confidence level.
        
        Args:
            confidence (float): Confidence percentage
            
        Returns:
            str: Confidence level description
        """
        if confidence >= 80:
            return "Very High"
        elif confidence >= 60:
            return "High"
        elif confidence >= 40:
            return "Medium"
        elif confidence >= 20:
            return "Low"
        else:
            return "Very Low"
