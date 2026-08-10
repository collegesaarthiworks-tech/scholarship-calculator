import streamlit as st
import pandas as pd
import requests

# Set up web page look
st.set_page_config(page_title="SRMS IBS Scholarship Calculator", page_icon="🎓", layout="centered")

# --- APNI GOOGLE SHEET KI LINK YAHA DALREIN ---
# Is double quote ke andar apni share ki hui google sheet ki poori link paste kar dein
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1lhCLlgirfhbVTZmCGLWS-4ifawuf9942-u3PH5WGc2Q/edit?usp=sharing"

st.title("🎓 SRMS IBS Scholarship Eligibility Checker")
st.write("Enter your details below to check your eligible tuition fee scholarship instantly.")

# Form Fields
with st.form("scholarship_form", clear_on_submit=True):
    name = st.text_input("Full Name", placeholder="Enter student name")
    mobile = st.text_input("Mobile Number", max_chars=10, placeholder="Enter 10-digit mobile number")
    course = st.selectbox("Select Course", ["BCA", "BBA", "MBA"])
    percentage = st.number_input("12th / Graduation Percentage (Upto 75%)", min_value=0.0, max_value=100.0, value=70.0, step=0.1)
    visit_day = st.selectbox("Preferred Campus Visit Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    
    submit_button = st.form_submit_button("Check My Scholarship Amount")

# System Processing
if submit_button:
    if not name or not mobile or len(mobile) < 10 or not mobile.isdigit():
        st.error("⚠️ Please enter a valid Name and 10-digit Mobile Number.")
    else:
        sch_type = "Standard Merit Basis"
        discount = "To be verified by Counselors"
        
        if course == "BCA":
            if percentage <= 75.0:
                sch_type = "15% Tuition Fee Waiver (Upto 75% Bracket)"
                discount = "Rs. 23,175 (Total Course Saving)"
            else:
                sch_type = "Higher Merit Slab"
                discount = "Rs. 45,000 (Total Course Saving)"
        elif course == "BBA":
            if percentage <= 75.0:
                sch_type = "10% Tuition Fee Waiver (Upto 75% Bracket)"
                discount = "Rs. 15,450 (Total Course Saving)"
        elif course == "MBA":
            if percentage <= 75.0:
                sch_type = "25% Tuition Fee Waiver (Upto 75% Graduation)"
                discount = "Rs. 24,821 (Per Year Saving)"

        # Web storage execution logic
        st.success(f"🎉 Congratulations {name}!")
        st.balloons()
        st.metric(label="Your Eligible Discount Amount", value=discount)
        st.info(f"📋 Scheme Type: {sch_type}")
        st.write("📱 Our admission team will contact you shortly on your number to process the next steps.")

# Admin Panel for Counselors
st.markdown("---")
if st.checkbox("🔑 Counselor Admin Login"):
    password = st.text_input("Enter Password", type="password")
    if password == "srms123":
        st.write("📊 **Lead Sheet Database Access:**")
        st.write(f"🔗 [Click here to open and view all live leads in Excel format]({GSHEET_URL})")
