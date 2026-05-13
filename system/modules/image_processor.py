"""
Image Processor Module
Handles face detection and image preprocessing using OpenCV.
Implements multi-method face detection with Haar Cascade and MTCNN fallback.
"""

import cv2
import numpy as np
from typing import Tuple, Optional, List


class ImageProcessor:
    """
    Handles image processing operations including face detection and preprocessing.
    """
    
    def __init__(self):
        """Initialize face detection cascades."""
        # Load Haar Cascade classifier for face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # MTCNN detector will be loaded lazily if needed
        self.mtcnn_detector = None
    
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load image from file path.
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            np.ndarray: Loaded image or None if failed
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Failed to load image")
            return image
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return None
    
    def detect_face_haar(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces using Haar Cascade classifier.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            List of face bounding boxes (x, y, width, height)
        """
        # Convert to grayscale for Haar Cascade
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply histogram equalization for better detection
        gray = cv2.equalizeHist(gray)
        
        # Detect faces with optimized parameters
        # scaleFactor: 1.1 for better sensitivity
        # minNeighbors: 6 for balance between false positives and detection rate
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=6,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        return faces.tolist() if len(faces) > 0 else []
    
    def detect_face_mtcnn(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces using MTCNN (Multi-task Cascaded Convolutional Networks).
        Fallback method for cases where Haar Cascade fails.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            List of face bounding boxes (x, y, width, height)
        """
        try:
            # Lazy load MTCNN to avoid unnecessary dependency
            if self.mtcnn_detector is None:
                from mtcnn import MTCNN
                self.mtcnn_detector = MTCNN()
            
            # Convert BGR to RGB for MTCNN
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            detections = self.mtcnn_detector.detect_faces(rgb_image)
            
            # Convert MTCNN format to (x, y, w, h)
            faces = []
            for detection in detections:
                if detection['confidence'] > 0.9:  # High confidence threshold
                    x, y, w, h = detection['box']
                    faces.append((x, y, w, h))
            
            return faces
        except Exception as e:
            print(f"MTCNN detection failed: {str(e)}")
            return []
    
    def detect_face(self, image: np.ndarray, use_mtcnn_fallback: bool = True) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect face in image using multi-method approach.
        
        Args:
            image (np.ndarray): Input image
            use_mtcnn_fallback (bool): Whether to use MTCNN if Haar fails
            
        Returns:
            Tuple of (x, y, width, height) for detected face, or None if no face found
        """
        # Try Haar Cascade first (faster)
        faces = self.detect_face_haar(image)
        
        # If Haar fails and fallback is enabled, try MTCNN
        if len(faces) == 0 and use_mtcnn_fallback:
            print("Haar Cascade failed, attempting MTCNN fallback...")
            faces = self.detect_face_mtcnn(image)
        
        # Return first detected face (largest if multiple)
        if len(faces) > 0:
            # Sort by area (width * height) and return largest
            faces_sorted = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
            return faces_sorted[0]
        
        return None
    
    def preprocess_face(self, image: np.ndarray, face_box: Tuple[int, int, int, int], 
                       target_size: Tuple[int, int] = (48, 48)) -> np.ndarray:
        """
        Extract and preprocess face region for model input.
        
        Args:
            image (np.ndarray): Original image
            face_box (tuple): Bounding box (x, y, width, height)
            target_size (tuple): Target dimensions for resizing
            
        Returns:
            np.ndarray: Preprocessed face image
        """
        x, y, w, h = face_box
        
        # Add padding to face region (10% on each side)
        padding = int(max(w, h) * 0.1)
        x_start = max(0, x - padding)
        y_start = max(0, y - padding)
        x_end = min(image.shape[1], x + w + padding)
        y_end = min(image.shape[0], y + h + padding)
        
        # Extract face region
        face_region = image[y_start:y_end, x_start:x_end]
        
        # Convert to grayscale
        if len(face_region.shape) == 3:
            face_gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
        else:
            face_gray = face_region
        
        # Resize to target size
        face_resized = cv2.resize(face_gray, target_size, interpolation=cv2.INTER_AREA)
        
        # Apply histogram equalization for better contrast
        face_normalized = cv2.equalizeHist(face_resized)
        
        return face_normalized
    
    def validate_image(self, image: np.ndarray) -> bool:
        """
        Validate image quality and properties.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            bool: True if image is valid, False otherwise
        """
        if image is None or image.size == 0:
            return False
        
        # Check minimum dimensions
        height, width = image.shape[:2]
        if height < 48 or width < 48:
            return False
        
        # Check if image is too dark (average pixel value)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        avg_brightness = np.mean(gray)
        
        if avg_brightness < 20:  # Too dark
            return False
        
        return True
