# intelligent-invoice-parser
Intelligent Document AI system for extracting structured fields from noisy invoice images using OCR + layout rules.

## Problem
Extract structured fields from noisy invoice images (scanned, multilingual, low-quality) for financial automation.

## Solution Overview
This system uses OCR + layout-based rules + business heuristics to robustly extract key fields such as dealer name, asset cost, and horse power.

## Architecture
Image → OCR → Text + Bounding Boxes → Rule-based Extraction → Confidence Scoring → JSON Output

## Field Extraction Strategy
- Dealer Name: Top-of-document heuristic + fuzzy matching
- Horse Power: Regex near "HP"
- Asset Cost: TOTAL row priority + numeric normalization

## Handling No Ground Truth
Pseudo-labeling and heuristic validation were used to iteratively refine extraction logic.

## Tech Stack
- Python
- EasyOCR
- OpenCV
- Regex-based parsing

## Results
Works reliably on noisy government and scanned invoices with low OCR quality.
