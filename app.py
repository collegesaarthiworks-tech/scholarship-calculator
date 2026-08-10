import streamlit as st
import pandas as pd
import os

# Set up web page look
st.set_page_config(page_title="SRMS IBS Scholarship Calculator", page_icon="🎓", layout="centered")

# Lead file name
LEAD_FILE = "leads.csv"

# Title
st.title("🎓 SRMS IBS Scholarship Eligibility Checker")
st.write("Enter your details below to check your eligible tuition fee scholarship instantly.")

# Form Fields
with st.form("scholarship_form", clear_on_submit=True):
    name = st.text_input("Full Name", placeholder="Enter your name")
    mobile = st.text_input("Mobile Number", max_chars=10, placeholder="Enter 10-digit mobile number")
    course = st.selectbox("Select Course", ["BCA", "BBA", "MBA"])
    percentage = st.number_input("12th / Graduation Percentage", min_value=0.0, max_value=100.0, value=75.0, step=0.1)
    
    submit_button = st.form_submit_button("Check My Scholarship Amount")

# Processing Logic
if submit_button:
    if not name or not mobile or len(mobile) < 10 or not mobile.isdigit():
        st.error("⚠️ Please enter a valid Name and 10-digit Mobile Number.")
    else:
        # Calculate Scholarship
        sch_type, discount = "Standard Merit Basis", "To be verified by Counselors"
        
        if course == "BCA":
            if percentage >= 80:
                sch_type, discount = "Special flat slab", "Rs. 45,000 (Total Course Saving)"
            elif percentage <= 75:
                sch_type, discount = "15% Tuition Waiver", "Rs. 23,175 (Total Course Saving)"
        elif course == "BBA":
            if percentage <= 75:
                sch_type, discount = "10% Tuition Waiver", "Rs. 15,450 (Total Course Saving)"
        elif course == "MBA":
            if 75 <= percentage <= 80:
                sch_type, discount = "25% + 2nd Year Bonus", "Rs. 57,141 (Total Course Saving)"
            elif percentage < 75:
                sch_type, discount = "25% Tuition Waiver", "Rs. 49,641 (Total Course Saving)"

        # Save to DataFrame / CSV
        new_lead = {"Name": name, "Mobile": mobile, "Course": course, "Percentage": percentage, "Scheme": sch_type, "Discount": discount}
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
        st.write("📱 Our admission team will contact you shortly on your number to process the next steps.")

# Admin Panel Hidden at bottom to download your leads
st.markdown("---")
if st.checkbox("🔑 Counselor Admin Login"):
    password = st.text_input("Enter Password", type="password")
    if password == "srms123": # You can change this secret password
        if os.path.isfile(LEAD_FILE):
            leads_df = pd.read_csv(LEAD_FILE)
            st.write("📊 **Current Student Leads Captured:**")
            st.dataframe(leads_df)
            
            # Download button for Excel/CSV spreadsheet
            csv_data = leads_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Lead Database Excel", data=csv_data, file_name="captured_leads.csv", mime="text/csv")
        else:
            st.warning("No leads captured yet.")
