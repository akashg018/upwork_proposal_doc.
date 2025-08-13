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

def generate_proposal(job_description, skills):
    prompt = f"""
    Create a professional Upwork proposal with exactly this structure and format:

    Title: "Proposal: [Brief Project Description]"

    [Opening paragraph explaining the understanding of the project and proposed solution without any bullet points]

    Relevant Experience
    [A paragraph describing relevant technical achievements and project completions without mentioning years of experience or using bullet points. Focus on completed projects and their impacts.]

    Technical Implementation
    [A detailed paragraph explaining the technical approach and methodology. Include specific technologies and how they will work together. No bullet points or subheadings.]

    Delivery Plan
    Phase 1: [Single line describing initial phase]
    Phase 2: [Single line describing development phase]
    Phase 3: [Single line describing final phase]

    [Closing paragraph with a brief call to action for discussion]

    Use this information:
    Job Description: {job_description}
    Technical Skills to Consider: {skills}
    
    Important guidelines:
    - Keep the tone professional and confident
    - Focus on solutions and implementation details
    - Don't mention personal experience
    - Be specific and technical in the implementation section
    - Structure the content with clear headings
    - Ensure the proposal demonstrates deep understanding of the requirements
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
    ### Professional Upwork Proposal Generator
    
    This tool will generate a structured proposal with:
    - Project understanding and solution overview
    - Relevant technical experience section
    - Detailed technical implementation
    - Three-phase delivery plan
    - Professional call to action
    
    *All fields marked with * are required*
    """)
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Project Details")
        job_description = st.text_area(
            "Job Description *",
            placeholder="Paste the complete job description from Upwork here...\n\nMake sure to include:\n- Project requirements\n- Technical specifications\n- Timeline expectations\n- Budget information\n- Any specific deliverables",
            height=300
        )
    
    with col2:
        st.subheader("Technical Skills")
        skills = st.text_area(
            "Relevant Technical Skills & Tools *",
            placeholder="List the technical skills, tools, and technologies relevant to this project...\n\nExample:\n- Frontend: React, Vue.js\n- Backend: Node.js, Python\n- Database: MySQL, MongoDB\n- Tools: Docker, AWS\n- Frameworks: FastAPI, Express",
            height=300
        )
    
    if st.button("Generate Proposal"):
        if not job_description or not skills:
            st.error("Please fill in all required fields!")
            return
        
        with st.spinner("Generating your professional proposal..."):
            try:
                proposal = generate_proposal(
                    job_description,
                    skills
                )
                
                st.success("Proposal generated successfully!")
                
                # Display the generated proposal
                st.subheader("Generated Proposal")
                st.write(proposal)
                
                # Create and offer PDF download
                pdf_path = create_pdf(proposal, "")
                
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
