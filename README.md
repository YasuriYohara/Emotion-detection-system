# Emotion Detection from Facial Expressions

**Project:** PUSL3190 Computing Project  
**Program:** BSc (Hons) Computer Security  
**Student:** Yasuri Y Adhikarai (10953290)  
**Institution:** University of Plymouth

## Overview

A lightweight web-based application for detecting emotions from static facial images using deep learning. The system classifies facial expressions into seven universal emotion categories: happiness, sadness, anger, fear, surprise, disgust, and neutrality.

## Features

### Core Features
- **Static Image Upload**: Process single facial photographs without requiring camera access
- **Multi-Model Detection**: Haar Cascade with MTCNN fallback for robust face detection
- **Privacy-First Design**: Temporary-only processing, no persistent storage of uploaded images
- **Confidence Scoring**: Clear indication of prediction certainty
- **Responsive Interface**: Modern, mobile-friendly web UI
- **Secure Processing**: Input validation, file type restrictions, and secure file handling

### New Features
- **Personalized Advice Suggestions**: Receive tailored advice based on your detected emotion
- **Music Therapy Recommendations**: Curated YouTube playlists for emotional well-being
- **Emotion Diary**: Track your daily emotions with notes and confidence scores
- **Admin Panel**: Comprehensive dashboard for user management and system analytics
  - User management (activate/deactivate accounts)
  - View all diary entries
  - System statistics and metrics
- **User Authentication**: Secure login system with email/username support

## Technology Stack

- **Backend**: Python 3.10, Flask 2.3
- **Computer Vision**: OpenCV 4.8
- **Emotion Recognition**: FER library, DeepFace
- **Deep Learning**: TensorFlow 2.10
- **Frontend**: HTML5, CSS3, JavaScript

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the repository**

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

## Usage

### For Regular Users
1. **Register/Login**: Create an account or log in with your credentials
2. **Detect Emotion**: 
   - Click "Choose File" to select a facial image (JPEG or PNG format)
   - Click "Detect Emotion" to process the image
   - View the predicted emotion and confidence score
3. **Get Personalized Advice**: Receive emotion-specific guidance and suggestions
4. **Music Therapy**: Access curated YouTube playlists for your emotional state
5. **Save to Diary**: Add detection results to your personal emotion diary with notes
6. **Track Emotions**: View your emotion history in the Diary section

### For Administrators
**Admin Credentials:**
- **Email**: admin@gmail.com
- **Password**: admin123

**Admin Features:**
1. Access the Admin Panel from the navigation menu
2. View system statistics (total users, active users, diary entries)
3. Manage user accounts (activate/deactivate)
4. Monitor recent diary entries across all users
5. Delete user accounts if necessary

## Supported Emotions

- 😊 Happiness
- 😢 Sadness
- 😠 Anger
- 😨 Fear
- 😲 Surprise
- 🤢 Disgust
- 😐 Neutral

## Security Considerations

- File type validation (JPEG/PNG only)
- Maximum file size limits
- Temporary file processing only
- No persistent storage of facial images
- Input sanitization with secure_filename()

## System Limitations

- Optimized for frontal face orientations
- Performance degrades with low illumination or significant blur
- Single-face processing (processes first detected face)
- Requires clear, unobstructed facial features

## Project Structure

```
SYSTEM/
├── app.py                      # Flask application entry point
├── modules/
│   ├── image_processor.py      # OpenCV face detection and preprocessing
│   ├── emotion_classifier.py   # Emotion detection model interface
│   └── file_manager.py         # Temporary file handling
├── static/
│   ├── css/
│   │   └── style.css           # Application styling
│   └── js/
│       └── script.js           # Client-side interactions
├── templates/
│   ├── index.html              # Upload interface
│   └── result.html             # Result display page
├── temp/                       # Temporary upload directory
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Development Methodology

This project follows an Agile development approach with iterative sprints, allowing for continuous refinement based on testing feedback and model performance evaluation.

## License

Academic project for educational purposes.

## Acknowledgments

- FER2013 Dataset (Kaggle, 2024)
- OpenCV Library
- FER and DeepFace Libraries
- Flask Framework
