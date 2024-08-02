from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Command to run the AYS System
# streamlit run recuiter.py

API_KEY='YOUR_KEY'
genai.configure(api_key=API_KEY)

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def gemini_jd_response(input,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


resume_gist = st.button("Tell Me About the Resume")
resume_match = st.button("Percentage match")
create_jd= st.button("Create Job Description")

resume_gist_prompt = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

resume_match_prompt = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

create_jd_prompt = """
You are a skilled Hiring Manager with deep understanding of data science, software engineering concepts and knowdlege on niche technology,
your task is to create a job desciption for the given company and for the role.
Response should have below sections:
- About the job
- Responsibilities
- Qualifications 
- Skills
"""

if resume_gist:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(resume_gist_prompt,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif resume_match:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(resume_match_prompt,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
elif create_jd:
    response=gemini_jd_response(create_jd_prompt,input_text)
    st.subheader("The Repsonse is")
    st.write(response)

   




