# 🧾 Intelligent Invoice Parser  
### GenAI Track – Convolve 4.0

> A practical, end-to-end **Document AI system** for extracting structured data from real-world **invoice and quotation images**, built with a strong focus on **robustness, explainability, and low-cost inference**.

---

## 🧠 Why this project?

In real enterprise workflows (banking, lending, compliance), documents rarely arrive as clean PDFs.  
Instead, they look like this 👇

<p align="center">
  <img src="docs/images/raw_invoice.png" width="400"/>
</p>

They are:
- Scanned images 📸  
- Government / PSU quotations 🏛️  
- Dealer invoices with inconsistent layouts 🧾  
- Noisy, low-quality OCR text  

This project is built for **that reality**, not idealized datasets.

---

## 🎯 What does the system extract?

For every document image, we extract:

- **Dealer Name**
- **Model Name** *(only if explicitly present — no hallucination)*
- **Horse Power (HP)** *(only if explicitly present)*
- **Asset Cost**
- **Signature** → presence + bounding box
- **Stamp** → presence + bounding box
- **Document-level confidence score**

All results are returned as structured JSON.

---

## 🧩 System Architecture

<p align="center">
  <img src="docs/images/architecture.png" width="700"/>
</p>


Each layer is **modular**, **replaceable**, and **independently testable**.

---

## 🔍 OCR Layer (EasyOCR)

<p align="center">
  <img src="docs/images/ocr_overlay.png" width="500"/>
</p>

- CPU-only OCR
- Handles skewed scans, mixed fonts, and noisy text
- Outputs text lines with bounding boxes

We deliberately chose a **lightweight OCR setup** to keep inference cost low.

---

## ✍️ Text Extraction (Design Choices)

### Dealer Name Extraction

<p align="center">
  <img src="docs/images/dealer_extraction.png" width="500"/>
</p>

- Detects **Government / PSU documents** using keywords like  
  *corporation*, *undertaking*, *department*
- Filters out phone numbers and numeric-heavy OCR noise
- Private dealers matched using **fuzzy matching** against a master list

This PSU vs private distinction turned out to be **critical in real data**.

---

### Model Name & Horse Power

- Extracted **only when explicitly present**
- Exact matching + regex
- Returned as `null` when absent → **no hallucination**

This conservative design improves trustworthiness.

---

## 👁️ Vision Module: Stamp & Signature

### Why vision?

Stamps and signatures are **visual trust signals** and cannot be reliably extracted using OCR alone.

<p align="center">
  <img src="docs/images/stamp_signature_boxes.png" width="500"/>
</p>

---

### 🧠 Hybrid Vision Strategy (Key Idea)

We use a **two-layer vision approach**:

#### 1️⃣ YOLOv8-Nano (ML-based)
- Trained using **pseudo-labels**
- Lightweight and CPU-friendly
- No manual annotation required

#### 2️⃣ OpenCV Heuristic Fallback
- Used when YOLO is uncertain
- Prevents excessive false negatives
- Ensures system robustness

> This hybrid approach balances **learning-based vision** with **engineering reliability**.

---

## 🏷️ Pseudo-Labeling & YOLO Training

<p align="center">
  <img src="docs/images/pseudo_labels.png" width="500"/>
</p>

- Initial stamp/signature boxes generated via OpenCV heuristics
- Converted automatically into YOLO label format
- Empty label files included as negative samples
- YOLOv8-Nano trained on this pseudo-labeled dataset

🎯 **Goal:**  
Demonstrate a scalable upgrade path — not chase benchmark mAP scores on limited data.

---

## 📊 Confidence Scoring (Explainable)

<p align="center">
  <img src="docs/images/confidence_plot.png" width="500"/>
</p>
Image
↓
OCR (EasyOCR)
↓
Text Lines
↓
Text Extraction Layer
├── Dealer Name (PSU-aware + fuzzy matching)
├── Model Name (exact match, no hallucination)
├── Horse Power (regex-based)
├── Asset Cost (numeric heuristics)
↓
Vision Layer (Hybrid)
├── YOLOv8 (pseudo-labeled)
└── OpenCV heuristic fallback
↓
Context-Aware Confidence Scoring
↓
Final JSON Output

Confidence is computed using **field-level signals + document context**:

- Government docs often omit model/HP → not penalized
- Vision failures do not zero out confidence
- Business-critical fields (dealer, cost) matter more
- Weights are normalized dynamically

This produces **honest, conservative confidence scores**.

---

## 📈 Error Analysis & Diagnostics

<p align="center">
  <img src="docs/images/error_analysis.png" width="500"/>
</p>

Observed patterns:
- OCR noise affecting dealer formatting
- Vision under-detection on low-contrast stamps
- Legitimate absence of model/HP in PSU documents

Mitigations:
- PSU-aware dealer logic
- Hybrid vision fallback
- Conservative extraction to avoid hallucination

---

## 💰 Low-Cost Inference Philosophy

<p align="center">
  <img src="docs/images/cost_breakdown.png" width="400"/>
</p>

- CPU-only execution
- Fully open-source stack:
  - EasyOCR
  - OpenCV
  - RapidFuzz
  - YOLOv8 (Ultralytics)
- No cloud APIs
- No paid LLMs

💸 **Estimated cost:** ~\$0.002 per document

---

## 📂 Project Structure


intelligent-invoice-parser/
├── ocr/
├── extraction/
├── vision/
│ ├── yolo_detector.py
│ ├── signature.py
│ └── stamp.py
├── postprocess/
│ └── confidence.py
├── analysis/
│ ├── predictions.json
│ └── generate_yolo_labels.py
├── data/
│ ├── images/
│ └── master/
├── docs/
│ └── images/
└── README.md



---

## ⚠️ Limitations & Future Work

- Larger labeled dataset for stronger YOLO performance
- Canonical normalization for similar PSU entity names
- Layout-aware extraction using document structure
- Faster OCR via image resizing and caching

---

## 🏁 Final Note

This project is intentionally **engineering-first**.

Rather than over-optimizing models, we focused on:
- robustness  
- explainability  
- modularity  
- realistic deployment constraints  

The result is a system designed to **grow into production**, not just pass a demo.

---

*Built for real documents, not perfect ones.*
