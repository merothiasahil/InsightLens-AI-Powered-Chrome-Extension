# 🧠 InsightLens – AI-Powered Content Analyzer Chrome Extension

<p align="center">
  <img src="extension/icons/icon128.png" alt="InsightLens Logo" width="200">
</p>

InsightLens is a browser-native Chrome Extension that allows users to instantly analyze content from text, images, URLs, or YouTube videos using advanced AI. It combines OCR, summarization, sentiment analysis, translation, and word cloud generation in one seamless tool.

## 🚀 Features

- 📜 **Text Summarization** (BART)
- 💬 **Sentiment Analysis** (RoBERTa)
- 🖼 **OCR from Screenshots** (Tesseract)
- 🌐 **Web Article Scraping & Analysis**
- 🎥 **YouTube Transcript Fetching & Translation** (Hindi → English)
- ☁️ **Keyword Visualization** (WordCloud)
- 📸 **Snipping Tool Integration**
- ⚡ **Right-click Text → Instant Insight**

## 🧠 How It Works

### 🔄 User Workflow

#### ➤ Method 1: Text Analysis
1. *User selects any text on a webpage*
2. *Right-click → Click "Analyze with InsightLens"*
3. *Extension popup opens automatically*
4. *Summarized content displayed with sentiment analysis and wordcloud*

#### ➤ Method 2: Image Analysis (OCR)
1. *User clicks "🖼 Analyze Image" button in extension*
2. *Custom snipping overlay appears on screen*
3. *User selects region of image to analyze*
4. *OCR extracts text → Summary → Sentiment → WordCloud displayed*

#### ➤ Method 3: YouTube Video Analysis
1. *User pastes YouTube URL in extension*
2. *Clicks "📺 Analyze YouTube" button*
3. *Transcript fetched and translated (if in Hindi)*
4. *Comprehensive summary with sentiment analysis displayed*

#### ➤ Method 4: Web Article Analysis
1. *User pastes article URL in extension*
2. *Clicks "🔗 Analyze URL" button*
3. *Content scraped and cleaned automatically*
4. *Full analysis results displayed in extension popup*

## 📂 Folder Structure

```
InsightLens/
├── assets/
│   ├── screenshots/
│   │   ├── extension-popup.jpg      # Main extension interface
│   │   ├── final-output.jpg         # Analysis results display
│   │   ├── ocr.jpg                  # OCR processing demo
│   │   └── text-summary-result.jpg  # Text summarization output
├── extension/
│   ├── popup.html
│   ├── popup.js
│   ├── style.css
│   ├── background.js
│   ├── contentScript.js
│   ├── manifest.json                # Manifest V3 for Chrome Extension
│   └── icons/
│       └── icon128.png
├── backend/
│   ├── app.py                       # Main Flask app
│   ├── routes.py                    # All route definitions
│   └── services/                    # Modular services
│       ├── ocr.py
│       ├── summarizer.py
│       ├── sentiment.py
│       ├── transcript.py
│       ├── translator.py
│       ├── webscraper.py
│       └── wordcloud_gen.py
└── README.md
```

## 💾 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jatin019/InsightLens-AI-Powered-Chrome-Extension.git
cd insightlens
```

### 2. Setup Tesseract OCR (Required)

🧠 Tesseract is used for extracting text from images.

#### ➤ Windows:
1. Download installer: https://github.com/tesseract-ocr/tesseract
2. Install and note the path (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`)
3. In `ocr.py`, set:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

#### ➤ Ubuntu/Linux:

```bash
sudo apt update
sudo apt install tesseract-ocr
```

### 3. Backend Setup (Flask API)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

🔁 **Run the Flask App:**

```bash
python app.py
```

Flask backend will start at: http://localhost:5000

### 4. Load the Chrome Extension

**Steps:**
1. Go to `chrome://extensions/`
2. Enable **Developer Mode** (top-right)
3. Click **"Load Unpacked"**
4. Select the `extension/` folder inside the project

💡 Now you'll see the 🧠 **InsightLens** icon in your Chrome toolbar.

## ▶️ Running the Project – Full Pipeline

```bash
# Step 1 – Clone repo
git clone https://github.com/your-username/insightlens
cd insightlens

# Step 2 – Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Step 3 – Load the extension
# Go to chrome://extensions/ → Enable Developer Mode → Load unpacked → Select extension/
```

Now the backend is running and the extension is live. You can right-click text, analyze images, paste YouTube or article URLs directly in the extension popup.

## 🧪 Live Demo Screenshots

### 📱 Extension Interface in Action
*User opens the InsightLens extension popup*
<p align="center">
  <img src="assets/screenshots/extension-popup.jpg" alt="InsightLens Extension Interface" width="400">
</p>

### 🔤 Text Analysis Results
*User selects text → Extension analyzes and displays summary*
<p align="center">
  <img src="assets/screenshots/text-summary-result.jpg" alt="Text Analysis Result" width="500">
</p>

### 🖼️ OCR Processing Demo
*User captures screenshot → OCR extracts text → Analysis displayed*
<p align="center">
  <img src="assets/screenshots/ocr.jpg" alt="OCR Processing Demo" width="500">
</p>

### 📊 Final Analysis Output
*Complete analysis results with summary, sentiment, and wordcloud*
<p align="center">
  <img src="assets/screenshots/final output.jpg" alt="Complete Analysis Results" width="500">
</p>

### 📋 Analysis Results Display
*Extension shows comprehensive analysis including:*
- ✅ **Summary**: Key points extracted
- ✅ **Sentiment**: Positive/Negative/Neutral detection  
- ✅ **WordCloud**: Visual keyword representation
- ✅ **Translation**: Hindi → English (for YouTube)

## 📈 Future Scope

- 🌍 Support for more languages (e.g., French, Arabic, Punjabi)
- 🗣 Add voice input via Whisper/Google STT
- 🔍 Auto-monitor news for real-time summarization
- 🧠 Personalized summaries based on tone/style
- 📌 On-hover insights or wordcloud overlays on live pages

## 📄 License

MIT License – Open for academic and personal use.
