import streamlit as st
import pandas as pd
import os

# Web page configuration
st.set_page_config(page_title="SRMS IBS Scholarship Calculator", page_icon="🎓", layout="centered")

# Lead database file name
LEAD_FILE = "leads.csv"

# Title & Description
st.title("🎓 Admission Saarthi Scholarship Eligibility Checker for SRMS IBS , LUCKNOW")
st.write("Enter your details below to check your eligible tuition fee scholarship instantly.")

# Form Fields
with st.form("scholarship_form", clear_on_submit=True):
    name = st.text_input("Full Name", placeholder="Enter student name")
    mobile = st.text_input("Mobile Number", max_chars=10, placeholder="Enter 10-digit mobile number")
    course = st.selectbox("Select Course", ["BCA", "BBA", "MBA"])
    percentage = st.number_input("12th / Graduation Percentage (Upto 75%)", min_value=0.0, max_value=100.0, value=70.0, step=0.1)
    
    # Campus Visit Dropdown
    visit_day = st.selectbox("Preferred Campus Visit Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    
    submit_button = st.form_submit_button("Check My Scholarship Amount")

# Processing Logic based on Official Document
if submit_button:
    if not name or not mobile or len(mobile) < 10 or not mobile.isdigit():
        st.error("⚠️ Please enter a valid Name and 10-digit Mobile Number.")
    else:
        sch_type = "Standard Merit Basis"
        discount = "To be verified by Counselors"
        
        # 1. BCA Scholarship Logic
        if course == "BCA":
            if percentage <= 75.0:
                sch_type = "15% Tuition Fee Waiver (Upto 75% Bracket)"
                discount = "Rs. 7,725 (Per Year Saving)"
            else:
                sch_type = "Higher Merit Slab"
                discount = "Rs. 15,000 (Per Year Saving as per 80% rule)"
                
        # 2. BBA Scholarship Logic        
        elif course == "BBA":
            if percentage <= 75.0:
                sch_type = "10% Tuition Fee Waiver (Upto 75% Bracket)"
                discount = "Rs. 5,150 (Per Year Saving)"
            else:
                sch_type = "Merit Slab"
                discount = "As per 12th Marks Policy"
                
        # 3. MBA Scholarship Logic (Flat 25% shown directly)
        elif course == "MBA":
            if percentage <= 75.0:
                sch_type = "25% Tuition Fee Waiver (Upto 75% Graduation)"
                discount = "Rs. 24,821 (Per Year Saving)"
            else:
                sch_type = "High Merit Bracket"
                discount = "To be reviewed by Admission Head"

        # Save lead data to DataFrame / CSV (Including Visit Day)
        new_lead = {
            "Name": name, 
            "Mobile": mobile, 
            "Course": course, 
            "Percentage": percentage, 
            "Preferred Visit Day": visit_day,
            "Scheme": sch_type, 
            "Discount": discount
        }
        df = pd.DataFrame([new_lead])
        
        if not os.path.isfile(LEAD_FILE):
            df.to_csv(LEAD_FILE, index=False)
        else:
            df.to_csv(LEAD_FILE, mode='a', header=False, index=False)

        # Show Results to Student
        st.success(f"🎉 Congratulations {name}!")
        st.balloons()
        st.metric(label="Your Eligible Discount Amount", value=discount)
        st.info(f"📋 Scheme Type: {sch_type}")
        st.write(f"📅 Your preferred campus visit day (**{visit_day}**) has been shared with the counselor team.")
        st.write("📱 Our admission team will contact you shortly on your number to process the next steps.")

# Admin Panel for Counselors
st.markdown("---")
if st.checkbox("🔑 Counselor Admin Login"):
    password = st.text_input("Enter Password", type="password")
    if password == "srms123":
        if os.path.isfile(LEAD_FILE):
            try:
                # Error-proof reading: ignores broken rows from previous versions
                leads_df = pd.read_csv(LEAD_FILE, on_bad_lines='skip')
                st.write("📊 **Current Student Leads Captured:**")
                st.dataframe(leads_df)
                
                csv_data = leads_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Lead Database Excel", data=csv_data, file_name="captured_leads.csv", mime="text/csv")
            except Exception as e:
                st.error("The old database file format is broken. Try submitting a new student form first to reset it.")
        else:
            st.warning("No leads captured yet.")
