import streamlit as st
from PIL import Image
import os
import cv2 as cv
import face_recognition as fr
from parse import parser
from thefuzz import fuzz
st.title("Image Input and Save Example")

save_dir = "saved_images"
os.makedirs(save_dir, exist_ok=True)

uploaded_id1 = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
uploaded_id2 = st.file_uploader("Upload an image2", type=["jpg", "jpeg", "png"])


selfie = st.camera_input("Take a selfie")

if selfie is not None:
    image = Image.open(selfie)
    st.image(image, caption="Captured Selfie", use_container_width=True)

    image.save("selfie.jpg")
    st.success(f"Selfie saved successfully.")
    selfie_img = cv.imread("selfie.jpg")
    selfie_img_rgb = cv.cvtColor(selfie_img, cv.COLOR_BGR2RGB)
    selfie_loc = fr.face_locations(selfie_img_rgb, model="cnn")
    for (top,right,bottom,left) in selfie_loc:
        cv.rectangle(selfie_img_rgb, (left, top), (right, bottom), (0, 0, 255), 2)
    selfie_enc = fr.face_encodings(selfie_img_rgb, selfie_loc)
    st.image(selfie_img_rgb, caption=f"Detected {len(selfie_loc)} face(s)", use_container_width=True)
  


if uploaded_id1 is not None:
    image = Image.open(uploaded_id1)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    save_path = os.path.join(save_dir, uploaded_id1.name)
    image.save(save_path)
    img = cv.imread(save_path)
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    data, loc, enc = parser(save_path)
    for (top,right,bottom,left) in loc:
        cv.rectangle(img_rgb, (left, top), (right, bottom), (0, 0, 255), 2)
    
    st.image(img_rgb, caption=f"Detected {len(loc)} face(s)", use_container_width=True)
    
    st.success(f"Image uploaded and saved at: {save_path}")
else:
    st.info("Please upload or capture an image to continue.")

if uploaded_id2 is not None:
    image2 = Image.open(uploaded_id2)
    st.image(image2, caption="Uploaded Image2", use_container_width=True)
    save_path = os.path.join(save_dir, uploaded_id2.name)
    image2.save(save_path)
    img2 = cv.imread(save_path)
    img_rgb2 = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
    data2, loc2, enc2 = parser(save_path)
    for (top,right,bottom,left) in loc2:
        cv.rectangle(img_rgb2, (left, top), (right, bottom), (0, 0, 255), 2)
    
    st.image(img_rgb2, caption=f"Detected {len(loc2)} face(s)", use_container_width=True)
    
    st.success(f"Image uploaded and saved at: {save_path}")

else:
    st.info("Please upload or capture an image2 to continue.")

tot_score = 0
kyc_pass = 0
button = st.button("Compute Score: ")
if button == True and uploaded_id1 is None and uploaded_id2 is None:
    st.info("upload atleast one Document....")
elif button == True and uploaded_id1 is not None and uploaded_id2 is None:
    
    if len(loc) == 0:
        st.info("face cant be recognised upload clear photo again")
    else:
        st.info("Only one id is uploaded, computing Score.....")
        distance = fr.face_distance([enc], selfie_enc[0])[0]
        st.write(distance,tot_score)
        if(distance < 0.6): tot_score = 50

elif button == True and uploaded_id1 is None and uploaded_id2 is not None:
    if len(loc2) == 0:
        st.info("face cant be recognised upload clear photo again")
    else:
        st.info("Only one id is uploaded, computing Score.....")
        distance = fr.face_distance([enc2],selfie_enc[0])[0]
        st.write(distance,tot_score)
        if distance < 0.6: tot_score = 50

elif button == True and uploaded_id1 is not None and uploaded_id2 is not None:
    scores = {}
    fields = ['name', 'dob', 'gender', 'address', 'father_name', 'husband_name']
    field_score = [30, 30, 10, 0, 10, 20]
    for field,score in zip(fields,field_score):
        val1 = data.get(field)
        val2 = data2.get(field)
        if val1 and val2:
            if field in ['dob', 'address']:
                scores[field] = fuzz.partial_ratio(val1, val2)
            else:
                scores[field] = fuzz.token_sort_ratio(val1, val2)
            tot_score += int(scores[field]*score/100)
        else:
            scores[field] = None
    distance = -1
    distance2 = -1
    tot_score = int(tot_score*70/100)
    if len(loc)>0 or len(loc2)>0:
        if len(loc) > 0:
            distance = fr.face_distance([enc],selfie_enc[0])[0]
        if len(loc2) > 0:
            distance2 = fr.face_distance([enc2],selfie_enc[0])[0]
    if distance != -1 and distance2 != -1:
        if distance <0.65: tot_score += 15
        if distance2 < 0.65: tot_score += 15
    elif distance != -1 and distance2 == -1:
        if distance< 0.65:
            tot_score += 20
    elif distance == -1 and distance2 != -1:
        if distance2 < 0.65: 
            tot_score += 20
    st.write(scores,distance,distance2,tot_score)

    






