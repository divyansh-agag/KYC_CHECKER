import cv2
import pytesseract
import re
import os
import json
from openai import OpenAI
import face_recognition
from thefuzz import fuzz
def parser(image_path):
    bgr_image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB) 
    image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)

    text = pytesseract.image_to_string(image, lang = "eng")


    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key="YOUR_HF_TOKEN",
    )

    print(text+"\n\n\n\n")

    prompt = f'''You are an intelligent KYC document parsing assistant.

    Your task is to extract personal information from OCR text of any Indian government ID document (Aadhaar, PAN, Voter ID, Passport, etc.).

    ### Instructions:
    1. Carefully analyze the OCR text provided below.
    2. Extract **only verified information** for the following fields:
    - Full Name
    - Father's Name (only if there is a clear marker like "S/O", "Father's Name", "Parent Name", "Guardian Name" nearby)
    - Husband's Name (only if the person is female and a marker like "H/O", "Husband's Name" is present)
    - Date of Birth (DOB)
    - Gender (Male/Female/Other)
    - Address (full address if clearly present)
    3. **Do not hallucinate any information**. If a field is not clearly present, return `null` for that field.
    4. Correct minor OCR errors if obvious.
    5. Return the output **strictly in JSON format** as below:


    "name": "",
    "father_name": null,
    "husband_name": null,
    "dob": null,
    "gender": null,
    "address": null

    ### OCR Text:
    {text}'''


    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-70B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for OCR KYC document parsing."},
            {"role": "user", "content": prompt}
        ],
        temperature=0 
    )
    llm_ans=completion.choices[0].message.content

    json_pattern = "\{([^}]*)\}"

    json_ = re.search(json_pattern, llm_ans)
    if json_:
        json_text = "{" + json_.group(1) + "}"  
        json_text = json_text.replace("'", '"')
        data = json.loads(json_text)
    #name = data['name']

    #print(llm_ans)
    #print(name)
    
    face_loc = face_recognition.face_locations(rgb_image, model='cnn')
    if (len(face_loc) == 0):
        encoding = None
    else:
        encoding = face_recognition.face_encodings(rgb_image, face_loc)[0]
    return data,face_loc,encoding