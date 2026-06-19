# 📂 Intelligent PDF Document Classifier & Auto-Organiser

An end-to-end ML-powered system that **automatically classifies and organises PDF files** the moment they land in your Downloads folder — no manual sorting needed.

---

## 🧠 How It Works

```
New PDF Downloaded
       │
       ▼
 Watchdog detects file
       │
       ▼
 pdfplumber extracts text
       │
       ▼
 TF-IDF vectorises text
       │
       ▼
 LinearSVC predicts category
       │
       ▼
 File moved to labelled folder
```

---

## 📁 Project Structure

```
pdf-auto-organiser/
│
├── data/                        # Training data (auto-created by collector)
│   ├── resume/
│   ├── medical_report/
│   ├── question_paper/
│   ├── research_paper/
│   └── documentation/
│
├── app.py            # watchdog

│
├── model.pkl                    # Saved classifier (generated after training)
├── vectorizer.pkl               # Saved TF-IDF vectorizer (generated after training)
│
└── requirements.txt
```

---

## 🗂️ Supported Categories

| Category | Examples |
|---|---|
| `resume` | CVs, job applications, personal portfolios |
| `medical_report` | Clinical reports, WHO/CDC bulletins, health data |
| `question_paper` | CBSE papers, university exams, competitive exam PDFs |
| `research_paper` | ArXiv papers, journal articles, academic publications |
| `documentation` | Library docs, API references, technical manuals |
| `other` | Anything unreadable or unrecognised |

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone [https://github.com/your-username/Intelligent-PDF-Document-Classifier-Auto-Organiser]
cd pdf-auto-organiser
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your Downloads path

Open `file_organizer.py` and update this line:

```python
DOWNLOAD_PATH = Path(r"C:\Users\YourName\Downloads")   # Windows
# DOWNLOAD_PATH = Path("/home/yourname/Downloads")      # Linux/Mac
```

---

## 🚀 Usage


### Step 1 — Train the model

```bash
python train_model.py
```

**Output:**
```
[1/4] Loading PDFs …
  resume               → 39 usable PDFs
  medical_report       → 35 usable PDFs
  question_paper       → 39 usable PDFs
  research_paper       → 39 usable PDFs
  documentation        → 39 usable PDFs

  5-Fold CV Accuracy : 0.9743  ±  0.0121

[4/4] Test Accuracy : 0.9744

Classification Report
------------------------------------------------------------
                precision  recall  f1-score  support
  documentation     1.00    0.88      0.93        8
         resume     1.00    1.00      1.00        8
 medical_report     1.00    1.00      1.00        7
  question_paper    1.00    1.00      1.00        8
  research_paper    0.89    1.00      0.94        8

✓ Saved: model.pkl  |  vectorizer.pkl  |  label_encoder.pkl
```

---

### Step 3 — Start the file watcher

```bash
python file_organizer.py
```

```
Watching Downloads Folder...
```

Now just download any PDF — it will be **automatically classified and moved** within seconds.

**Before:**
```
Downloads/
├── report_2024.pdf
├── cv_john.pdf
├── transformer_paper.pdf
└── cbse_maths.pdf
```

**After:**
```
Downloads/
├── medical_report/
│   └── report_2024.pdf
├── resume/
│   └── cv_john.pdf
├── research_paper/
│   └── transformer_paper.pdf
└── question_paper/
    └── cbse_maths.pdf
```

---

## 🔬 Model Details

| Component | Choice | Reason |
|---|---|---|
| Text extraction | `pdfplumber` | Handles complex layouts, multi-column PDFs |
| Vectorizer | `TF-IDF` | Robust, fast, interpretable; captures domain vocabulary |
| N-gram range | `(1, 3)` | Captures phrases like "blood pressure", "time complexity" |
| Max features | `50,000` | Wide enough vocabulary without overfitting |
| Classifier | `LinearSVC` | Best accuracy/speed tradeoff for text classification |
| Class weights | `balanced` | Handles unequal samples per category gracefully |
| Validation | `5-Fold CV` | Confirms generalisation beyond a single train/test split |

### Results

```
Accuracy  : 97.4%
Macro-F1  : 97%

Confusion Matrix:
               resume  medical  qpaper  research  docs
resume              8        0       0         0     0
medical_report      0        7       0         0     0
question_paper      0        0       8         0     0
research_paper      0        0       0         8     0
documentation       0        0       1         0     7
```

---

## 📋 Requirements

```
pdfplumber
scikit-learn
watchdog
requests
```

Install all at once:

```bash
pip install pdfplumber scikit-learn watchdog requests
```


## 📝 Logs

The watcher writes a persistent log to `_organizer.log` inside your Downloads folder:

```
2025-06-10 14:32:01  INFO     New PDF detected (move): transformer_xl.pdf
2025-06-10 14:32:03  INFO     Classified  transformer_xl.pdf          →  research_paper
2025-06-10 14:32:03  INFO     Moved  →  Downloads/research_paper/transformer_xl.pdf
```

---

## 🛠️ Configuration Reference

| Variable | File | Default | Description |
|---|---|---|---|
| `DOWNLOAD_PATH` | `file_organizer.py` | `C:\Users\Sarisht Shreshth\Downloads` | Folder to watch |
| `MAX_PAGES` | both | `15` | Pages read per PDF for classification |
| `MIN_CHARS` | both | `100` | Minimum characters to attempt classification |
| `SETTLE_DELAY` | `app.py` | `2` seconds | Wait time after file appears (browser write finish) |




## 👤 Author

**Sarisht Shreshth**
[GitHub]([https://github.com/sarishtshreshth0/Intelligent-PDF-Document-Classifier-Auto-Organiser]) · [LinkedIn]([https://www.linkedin.com/in/sarisht-shreshth/]) · [CodeChef]([https://www.codechef.com/users/sarishtshresht])
