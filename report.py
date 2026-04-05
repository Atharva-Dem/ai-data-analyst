# report.py
# This file generates a professional business insights report
# using GPT-4o based on your dataset
# and exports it as a downloadable PDF

# report.py
# report.py
import os
from groq import Groq
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_report(df):

    summary = f"""
    Dataset shape: {df.shape[0]} rows and {df.shape[1]} columns
    Column names: {list(df.columns)}
    Statistical summary:
    {df.describe().to_string()}
    Missing values per column:
    {df.isnull().sum().to_string()}
    First 5 rows sample:
    {df.head().to_string()}
    """

    prompt = f"""
    You are a senior data analyst at a top consulting firm like Accenture or Deloitte.
    Analyze the following dataset summary and write a DETAILED professional business insights report.

    Dataset Summary:
    {summary}

    Write a FULL and DETAILED report with these exact sections.
    Each section MUST have multiple paragraphs or bullet points. Do NOT skip any section.

    1. Executive Summary
    Write 4-5 sentences giving a complete overview of the dataset, what it contains,
    its size, and what business area it covers.

    2. Key Findings
    Write at least 6-8 specific bullet points with actual numbers from the data.
    Example: average values, min/max, most common categories, distributions.

    3. Data Quality Assessment
    Write 3-4 sentences about missing values, data types, any anomalies or outliers,
    and whether the data is ready for analysis.

    4. Business Recommendations
    Write 4-5 detailed, actionable recommendations based on the findings.
    Each recommendation should be 2-3 sentences explaining what to do and why.

    5. Conclusion
    Write 3-4 sentences summarizing the overall findings and next steps.

    Be very specific, use actual numbers from the data, and write in a professional tone.
    Use only simple ASCII characters. No special symbols or unicode characters.
    Make this report at least 500 words long.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    report_text = response.choices[0].message.content
    return report_text


def clean_text(text):
    # Replace common unicode characters with ASCII equivalents
    replacements = {
        '\u2019': "'", '\u2018': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '-',
        '\u2022': '*', '\u2026': '...',
        '\u00e9': 'e', '\u00e0': 'a',
        '\u00fc': 'u', '\u00f6': 'o',
        '\u00e4': 'a', '\u00b0': ' degrees',
    }
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    # Final safety — encode to latin-1 replacing anything else
    text = text.encode('latin-1', 'replace').decode('latin-1')
    return text


def export_pdf(report_text):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)
    pdf.set_top_margin(20)
    pdf.set_auto_page_break(auto=True, margin=20)

    # Title
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.cell(0, 10, "AI Data Analysis Report", ln=True, align="C")
    pdf.ln(5)

    # Write content line by line
    pdf.set_font("Helvetica", size=10)
    for line in report_text.split('\n'):
        line = line.strip()
        if line == "":
            pdf.ln(3)
        else:
            line = clean_text(line)
            # Skip lines that are too long without spaces
            if len(line) > 0:
                try:
                    pdf.multi_cell(0, 6, line)
                except Exception:
                    # If a line still fails, skip it safely
                    pdf.ln(3)

    filename = "ai_report.pdf"
    pdf.output(filename)
    return filename