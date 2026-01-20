import os
import csv
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ✅ Save Attendance as CSV
def save_csv(records, subject: str, out_dir: str = "backend/app/static/uploads") -> str:
    """
    Save attendance records to a CSV file.
    Each record must contain: roll_no, name, status
    """
    os.makedirs(out_dir, exist_ok=True)
    today = date.today().isoformat()
    filename = f"{subject}_attendance_{today}.csv"
    path = os.path.join(out_dir, filename)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Roll No", "Name", "Subject", "Date", "Status"])
        for r in records:
            writer.writerow([
                r.get("roll_no", ""),
                r.get("name", ""),
                subject,
                today,
                r.get("status", "Present"),
            ])
    return path


# ✅ Save Attendance as PDF
def save_pdf(records, subject: str, out_dir: str = "backend/app/static/uploads") -> str:
    """
    Generate a PDF attendance report using ReportLab.
    Each record must contain: roll_no, name, status
    """
    os.makedirs(out_dir, exist_ok=True)
    today = date.today().isoformat()
    filename = f"{subject}_attendance_{today}.pdf"
    path = os.path.join(out_dir, filename)

    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 40, f"Attendance Report - {subject} - {today}")
    c.setFont("Helvetica", 12)

    # Column headings
    y = height - 80
    c.drawString(40, y, "Roll No")
    c.drawString(120, y, "Name")
    c.drawString(300, y, "Status")
    y -= 20

    # Records
    for r in records:
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 60
        c.drawString(40, y, str(r.get("roll_no", "")))
        c.drawString(120, y, str(r.get("name", "")))
        c.drawString(300, y, str(r.get("status", "Present")))
        y -= 20

    c.save()
    return path
