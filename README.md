# KYC_CHECKER

A prototype AI-powered KYC (Know Your Customer) checker that extracts information from government-issued documents and verifies user identity using face recognition.

This project combines **OCR**, **LLM-based data structuring**, **face recognition**, and **fuzzy text matching** to create a streamlined KYC verification workflow.  

---

#BEFORE RUNNING THE APPLICATION MAKE SURE TO GO TO parse.py andplace your HUGGING FACE TOKEN IN PLACWE OF "YOUR_HF_TOKEN" TO ACCESS THE OPEN-SOURCE MODEL....

## Features

- Upload and parse multiple types of KYC documents (e.g., Aadhaar, PAN)
- Capture a selfie and perform face matching with document photo
- Extract structured data from raw OCR text
- Fuzzy matching for text verification to handle small discrepancies
- Streamlit-based web interface
- Assigns a verification score based on fuzzy text and face matching

---

Upload two KYC documents (e.g., Aadhaar, PAN).

Each upload may take 10–15 seconds as the app performs face recognition.

Capture a selfie using the camera input.

Click the "Compute Score:" button to:

Parse the documents

Extract relevant information using a language model

Compare the selfie with document photos

Compute and display the verification score

***File Structure***

ui.py – Main Streamlit application

parse.py – Utility functions (e.g., parser()) used by ui.py

saved_images/ – Directory where uploaded/captured images are saved
