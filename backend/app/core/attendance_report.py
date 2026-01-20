import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import date

BASE_DIR = os.path.abspath(os.getcwd())
REPORT_DIR = os.path.join(BASE_DIR, "backend", "storage", "attendance_reports")
CSV_DIR = os.path.join(REPORT_DIR, "csv")
PDF_DIR = os.path.join(REPORT_DIR, "pdf")
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

def generate_csv(subject: str, present_students: list):
    """Generate CSV report for attendance."""
    if not present_students:
        print("⚠️ No students to include in CSV.")
        return None
    
    today = date.today()
    filename = f"{subject}_{today}.csv"
    filepath = os.path.join(CSV_DIR, filename)
    
    # Create DataFrame with department
    data = {
        "Roll No": [s["roll_no"] for s in present_students],
        "Name": [s["name"] for s in present_students],
        "Department": [s.get("department", "N/A") for s in present_students],  # Added department
        "Status": ["Present"] * len(present_students)
    }
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    print(f"✅ CSV report saved: {filepath}")
    return filepath

def generate_pdf(subject: str, present_students: list):
    """Generate PDF report for attendance."""
    if not present_students:
        print("⚠️ No students to include in PDF.")
        return None
    
    today = date.today()
    filename = f"{subject}_{today}.pdf"
    filepath = os.path.join(PDF_DIR, filename)
    
    # Create PDF
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, f"Attendance Report - {subject}")
    c.drawString(100, height - 70, f"Date: {today}")
    
    # Table Header with department
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "Roll No")
    c.drawString(120, height - 100, "Name")
    c.drawString(350, height - 100, "Department")  # Added department header
    c.drawString(480, height - 100, "Status")
    
    # Table Data with department
    y = height - 120
    c.setFont("Helvetica", 10)
    for student in present_students:
        c.drawString(50, y, student["roll_no"])
        c.drawString(120, y, student["name"])
        c.drawString(350, y, student.get("department", "N/A"))  # Added department data
        c.drawString(480, y, "Present")
        y -= 20
        if y < 50:  # New page if needed
            c.showPage()
            y = height - 50
    
    c.save()
    print(f"✅ PDF report saved: {filepath}")
    return filepath