import streamlit as st
import pandas as pd

# Web page configuration
st.set_page_config(page_title="SRMS IBS Scholarship Calculator", page_icon="🎓", layout="centered")

# --- INSTANT WEB PAGE MEMORY STORAGE ---
# This initializes a permanent list inside the web page container memory
if "web_database" not in st.session_state:
    st.session_state.web_database = [
        {
            "Name": "AYUSH",
            "Mobile": "8171666384",
            "Course": "BCA",
            "Percentage": 75.0,
            "Preferred Visit Day": "Monday",
            "Scheme": "15% Tuition Waiver",
            "Discount": "Rs. 23,175 (Total Course Saving)"
        }
    ]

# Title & Description
st.title("🎓 SRMS IBS Scholarship Eligibility Checker")
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
                discount = "Rs. 23,175 (Total Course Saving)"
            else:
                sch_type = "Higher Merit Slab"
                discount = "Rs. 45,000 (Total Course Saving)"
                
        # 2. BBA Scholarship Logic        
        elif course == "BBA":
            if percentage <= 75.0:
                sch_type = "10% Tuition Fee Waiver (Upto 75% Bracket)"
                discount = "Rs. 15,450 (Total Course Saving)"
            else:
                sch_type = "Merit Slab"
                discount = "As per 12th Marks Policy"
                
        # 3. MBA Scholarship Logic
        elif course == "MBA":
            if percentage <= 75.0:
                sch_type = "25% Tuition Fee Waiver (Upto 75% Graduation)"
                discount = "Rs. 24,821 (Per Year Saving)"
            else:
                sch_type = "High Merit Bracket"
                discount = "To be reviewed by Admission Head"

        # Append new lead dynamically to the live screen memory
        new_entry = {
            "Name": name.upper(), 
            "Mobile": mobile, 
            "Course": course, 
            "Percentage": percentage, 
            "Preferred Visit Day": visit_day,
            "Scheme": sch_type, 
            "Discount": discount
        }
        st.session_state.web_database.append(new_entry)

        # Show Results to Student
        st.success(f"🎉 Congratulations {name}!")
        st.balloons()
        st.metric(label="Your Eligible Discount Amount", value=discount)
        st.info(f"📋 Scheme Type: {sch_type}")
        st.write(f"📅 Your preferred campus visit day (**{visit_day}**) has been shared with the counselor team.")
        st.write("📱 Our admission team will contact you shortly on your number to process the next steps.")

# Admin Panel for Counselors (Always updates live on page refresh or submit)
st.markdown("---")
if st.checkbox("🔑 Counselor Admin Login"):
    password = st.text_input("Enter Password", type="password")
    if password == "srms123":
        st.write("📊 🎉 **Current Student Leads Captured (Live on Webpage):**")
        
        # Convert memory list directly into on-screen table
        leads_df = pd.DataFrame(st.session_state.web_database)
        st.dataframe(leads_df, use_container_width=True)
        
        # Immediate direct download link for the entire row system
        csv_data = leads_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Lead Database Excel", data=csv_data, file_name="web_leads.csv", mime="text/csv")
