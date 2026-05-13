# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

Open PowerShell in the SYSTEM directory and run:

```powershell
.\setup_env.ps1
```

Or manually:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python app.py
```

### Step 3: Open in Browser

Navigate to: **http://localhost:5000**

---

## 📸 Using the System

1. **Click "Choose File"** or drag and drop an image
2. **Select a facial photograph** (JPEG/PNG, max 10MB)
3. **Click "Detect Emotion"**
4. **View results** with confidence scores

---

## ✅ Best Practices for Accurate Results

- Use **well-lit** photographs
- Ensure **frontal face orientation**
- Avoid **sunglasses or masks**
- Use **clear, high-quality** images
- **Single person** per image works best

---

## 🔧 Troubleshooting

### Application won't start
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### No face detected
- Check image quality and lighting
- Ensure face is clearly visible
- Try a different photo angle

### Import errors
```bash
# Clear Python cache
Remove-Item -Recurse -Force __pycache__
Remove-Item -Recurse -Force modules\__pycache__

# Restart the application
python app.py
```

---

## 📊 Understanding Results

**Confidence Levels:**
- **80-100%**: Very high confidence - reliable result
- **60-80%**: High confidence - generally accurate
- **40-60%**: Medium confidence - use with caution
- **Below 40%**: Low confidence - consider retrying

**Emotion Scores:**
All seven emotions are scored. The highest score determines the prediction.

---

## 🛡️ Privacy & Security

- ✓ All images processed locally
- ✓ No cloud uploads or external API calls
- ✓ Files deleted immediately after processing
- ✓ No data retention or logging

---

## 📚 Project Information

**Course:** PUSL3190 Computing Project  
**Program:** BSc (Hons) Computer Security  
**Institution:** University of Plymouth  
**Student:** Yasuri Y Adhikarai (10953290)

---

## 📖 Additional Resources

- **Full Documentation:** See `README.md`
- **Installation Guide:** See `INSTALLATION_GUIDE.md`
- **Accuracy Details:** See `ACCURACY_IMPROVEMENTS.md`
- **Run Tests:** `python run_tests.py`

---

## 🎯 Supported Emotions

😊 Happiness | 😢 Sadness | 😠 Anger | 😨 Fear  
😲 Surprise | 🤢 Disgust | 😐 Neutral

---

**Need Help?** Check the full documentation or review error messages in the terminal.
