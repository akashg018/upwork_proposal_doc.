import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Set up the model
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_proposal(job_description, skills, experience, portfolio_links):
    prompt = f"""
    Create a professional Upwork proposal based on the following information:
    Job Description: {job_description}
    
    My Skills: {skills}
    
    My Experience: {experience}
    
    Portfolio Links: {portfolio_links}
    
    Generate a compelling, personalized proposal that:
    1. Starts with a strong hook
    2. Addresses the client's specific needs
    3. Highlights relevant skills and experience
    4. Includes a clear value proposition
    5. Ends with a strong call to action
    6. Maintains a professional yet friendly tone
    7. Is between 200-300 words
    """
    
    response = model.generate_content(prompt)
    return response.text

def create_pdf(proposal_text, client_info):
    pdf = FPDF()
    pdf.add_page()
    
    # Set up the PDF
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Professional Upwork Proposal", ln=True, align="C")
    pdf.ln(10)
    
    # Add date
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%B %d, %Y')}", ln=True)
    pdf.ln(10)
    
    # Add client information
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Client Information:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, client_info)
    pdf.ln(10)
    
    # Add proposal content
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Proposal:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, proposal_text)
    
    # Save the PDF
    pdf_path = "generated_proposal.pdf"
    pdf.output(pdf_path)
    return pdf_path

def main():
    st.set_page_config(page_title="Professional Upwork Proposal Generator", layout="wide")
    
    st.title("🚀 Professional Upwork Proposal Generator")
    st.markdown("""
    ### Generate High-Quality Upwork Proposals
    
    **How to use:**
    1. Paste the job posting details in the left column
    2. Add your professional information in the right column
    3. Click 'Generate Proposal' to create your customized proposal
    4. Download the proposal as a PDF
    
    *All fields marked with * are required*
    """)
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Project Details")
        job_description = st.text_area(
            "Job Description *",
            placeholder="Paste the complete job description from Upwork here...\n\nExample:\nLooking for a Python developer to build...",
            height=200
        )
        
        client_info = st.text_area(
            "Client Information (Optional)",
            placeholder="Add any specific details about the client or project requirements...\n\nExample:\n- Client's industry\n- Project budget\n- Timeline requirements\n- Previous work history",
            height=100
        )
    
    with col2:
        st.subheader("Your Information")
        skills = st.text_area(
            "Your Key Skills *",
            placeholder="List your relevant skills that match the job requirements...\n\nExample:\n- Python Development\n- Database Design\n- API Integration\n- Cloud Architecture",
            height=100
        )
        
        experience = st.text_area(
            "Relevant Experience *",
            placeholder="Describe your relevant experience for this specific job...\n\nExample:\n- Successfully delivered 3 similar projects\n- 5 years of experience in...\n- Specific achievements and metrics",
            height=100
        )
        
        portfolio_links = st.text_area(
            "Portfolio Links",
            placeholder="Add links to relevant work samples, GitHub repositories, or previous projects...\n\nExample:\n- https://github.com/yourusername/project\n- https://yourportfolio.com/project1",
            height=100
        )
    
    if st.button("Generate Proposal"):
        if not job_description or not skills or not experience:
            st.error("Please fill in all required fields!")
            return
        
        with st.spinner("Generating your professional proposal..."):
            try:
                proposal = generate_proposal(
                    job_description,
                    skills,
                    experience,
                    portfolio_links
                )
                
                st.success("Proposal generated successfully!")
                
                # Display the generated proposal
                st.subheader("Generated Proposal")
                st.write(proposal)
                
                # Create and offer PDF download
                pdf_path = create_pdf(proposal, client_info)
                
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                
                st.download_button(
                    label="Download Proposal as PDF",
                    data=pdf_bytes,
                    file_name="upwork_proposal.pdf",
                    mime="application/pdf"
                )
                
                # Clean up
                os.remove(pdf_path)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please make sure you have set up your GOOGLE_API_KEY in the .env file.")

if __name__ == "__main__":
    main()
