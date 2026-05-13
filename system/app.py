"""
Emotion Detection from Facial Expressions
Flask Web Application with Authentication

PUSL3190 Computing Project
BSc (Hons) Computer Security
University of Plymouth

Author: Yasuri Y Adhikarai (10953290)
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
import os
import sys
import re

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db, User
from modules.file_manager import save_temp, delete_temp, allowed_file, cleanup_temp_directory
from modules.image_processor import ImageProcessor
from modules.emotion_classifier import EmotionClassifier

# Initialize Flask application
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['UPLOAD_FOLDER'] = 'temp'
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-2024'  # Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emotion_detection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Initialize processors
image_processor = ImageProcessor()
emotion_classifier = EmotionClassifier(model_type='fer')

# Ensure temp directory exists
if not os.path.exists('temp'):
    os.makedirs('temp')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """Home page - public access"""
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        full_name = request.form.get('full_name', '').strip()
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append('Username can only contain letters, numbers, and underscores.')
        
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Please provide a valid email address.')
        
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists.')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Create new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            full_name=full_name
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            app.logger.error(f"Registration error: {str(e)}")
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Please provide both username and password.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=bool(remember))
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/home')
@login_required
def home():
    """Home page after login"""
    return render_template('home.html')


@app.route('/service')
@login_required
def service():
    """Emotion detection service page"""
    cleanup_temp_directory()
    return render_template('service.html')


@app.route('/about')
@login_required
def about():
    """About page"""
    return render_template('about.html')


@app.route('/contact')
@login_required
def contact():
    """Contact page"""
    return render_template('contact.html')


@app.route('/predict', methods=['POST'])
@login_required
def predict():
    """
    Handle emotion prediction from uploaded image.
    
    Returns:
        Rendered result page or error page
    """
    filepath = None
    
    try:
        # Check if file is present in request
        if 'image' not in request.files:
            return render_template('service.html', 
                                 error='No file uploaded. Please select an image.')
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return render_template('service.html', 
                                 error='No file selected. Please choose an image.')
        
        # Validate file type
        if not allowed_file(file.filename):
            return render_template('service.html', 
                                 error='Invalid file type. Please upload a JPEG or PNG image.')
        
        # Save file to temporary location
        try:
            filepath = save_temp(file)
        except ValueError as e:
            return render_template('service.html', error=str(e))
        
        # Load and validate image
        image = image_processor.load_image(filepath)
        if image is None:
            return render_template('service.html', 
                                 error='Failed to load image. Please ensure the file is a valid image.')
        
        # Validate image quality
        if not image_processor.validate_image(image):
            return render_template('service.html', 
                                 error='Image quality is insufficient. Please upload a clearer, well-lit image.')
        
        # Detect face in image
        face_box = image_processor.detect_face(image, use_mtcnn_fallback=True)
        
        if face_box is None:
            return render_template('service.html', 
                                 error='No face detected in the image. Please upload an image with a clear, frontal face.')
        
        # Preprocess face region
        face_processed = image_processor.preprocess_face(image, face_box)
        
        # Classify emotion
        result = emotion_classifier.classify_emotion(image=image, image_path=filepath)
        
        if result['error']:
            return render_template('service.html', error=result['error'])
        
        if result['emotion'] is None:
            return render_template('service.html', 
                                 error='Could not determine emotion. Please try another image.')
        
        # Get emoji and confidence level
        emoji = emotion_classifier.get_emotion_emoji(result['emotion'])
        confidence_level = emotion_classifier.get_confidence_level(result['confidence'])
        
        # Render result page
        return render_template('result.html', 
                             emotion=result['emotion'],
                             emoji=emoji,
                             confidence=result['confidence'],
                             confidence_level=confidence_level,
                             is_confident=result['is_confident'],
                             all_scores=result['all_scores'])
    
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return render_template('service.html', 
                             error=f'An unexpected error occurred: {str(e)}')
    
    finally:
        # Always delete temporary file
        if filepath:
            delete_temp(filepath)


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    flash('File size too large. Maximum allowed size is 10MB.', 'error')
    return redirect(url_for('service')), 413


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Internal server error: {str(error)}")
    flash('An internal server error occurred. Please try again.', 'error')
    return redirect(url_for('index')), 500


# Database initialization
def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")


if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run application
    # Debug mode should be False in production
    app.run(debug=True, host='127.0.0.1', port=5000)
