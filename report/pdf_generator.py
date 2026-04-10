from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("Code Review Report", styles['Title']))
    content.append(Spacer(1, 12))

    # Analysis
    content.append(Paragraph("Analysis", styles['Heading2']))
    content.append(Paragraph(f"Loops: {data['analysis']['loops']}", styles['BodyText']))
    content.append(Paragraph(f"Nesting Depth: {data['analysis']['max_nesting_depth']}", styles['BodyText']))
    content.append(Spacer(1, 12))

    # Suggestions
    content.append(Paragraph("Suggestions", styles['Heading2']))
    for s in data['suggestions']:
        content.append(Paragraph(f"- {s}", styles['BodyText']))
    content.append(Spacer(1, 12))

    # LLM Review
    content.append(Paragraph("AI Review", styles['Heading2']))
    llm_review = data.get('formatted_review')

    if isinstance(llm_review, dict):
        for section_name, items in llm_review.items():
            content.append(Paragraph(section_name, styles['Heading3']))
            for item in items:
                content.append(Paragraph(f"- {item}", styles['BodyText']))
            content.append(Spacer(1, 8))
    else:
        content.append(Paragraph(str(llm_review), styles['BodyText']))

    doc.build(content)