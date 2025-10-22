# KYC_CHECKER

A prototype AI-powered KYC (Know Your Customer) checker that extracts information from government-issued documents and verifies user identity using face recognition.

This project uses **OCR** to extract text from KYC documents, a **language model** to structure the text into JSON key-value pairs, and **face recognition** to compare the user's selfie with the document's photo. Additionally, **fuzzy text matching** is used to handle small discrepancies in document information.

---

## Features

- Upload and parse multiple types of KYC documents (e.g., Aadhaar, PAN)
- Capture a selfie and perform face matching with document photo
- Extract structured data from raw OCR text
- Fuzzy matching for text verification
- Streamlit-based web interface
- assign score based on fuzzy matching and face matching
---
parse.py contains utility fuction parser() for the ui.py 
to run application install following dependencies:

streamlit
opencv-python
face_recognition
pillow
thefuzz
numpy
after installation of these run ui.py with following command:
      ***streamlit run ui.py***
after running the application upload 2 docs and one selfie after each upload it may freeze for 10-15 secs as it will be doing face_recognition on the image 
after completing the upload click on button "Compute Score: " it will take some time to parse the documents and extarct relevent information using an llm and after that it will show output..
