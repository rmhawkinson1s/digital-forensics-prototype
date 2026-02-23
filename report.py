from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import json
import os
from typing import Any, Dict, List

def generate_report(
    title: str = "Court Style System Report (Prototype)",
    out_path: str = "artifacts/report.pdf",
    log_path: str = "artifacts/audit_log.json",
) -> None:
    """Generate a simple PDF report from the audit log (FR-14)."""
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"No audit log found at {log_path}")

    with open(log_path, "r", encoding="utf-8") as f:
        logs: List[Dict[str, Any]] = json.load(f)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    c = canvas.Canvas(out_path, pagesize=LETTER)
    width, height = LETTER

    y = height - 72  # 1 inch top margin

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y, title)
    y -= 28

    c.setFont("Helvetica", 10)
    c.drawString(72, y, "Generated from structured audit logs (who/when/what).")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Audit Log Excerpt")
    y -= 18

    c.setFont("Helvetica", 9)
    for log in logs:
        line = f"{log.get('timestamp','?')} | {log.get('action','?')} | {str(log.get('details',''))[:90]}"
        c.drawString(72, y, line)
        y -= 14
        if y < 72:  # bottom margin
            c.showPage()
            y = height - 72
            c.setFont("Helvetica", 9)

    c.save()
    print(f"Report generated: {out_path}")
