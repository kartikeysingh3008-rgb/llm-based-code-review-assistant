import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
from rules.engine import generate_suggestions
from llm.reviewer import get_llm_review, clean_response, format_review
from report.pdf_generator import generate_pdf
from scorer.score import calculate_score, classify_score
from parser.ast_parser import analyze_code
from contact_handler import validate_contact_form


load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)

# Global storage
latest_report = {}

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    global latest_report

    code = request.form.get('code')

    if not code or code.strip() == "":
        return render_template('index.html', error="No code provided")

    analysis = analyze_code(code)

    if "error" in analysis:
        return render_template('index.html', error=analysis["error"])

    suggestions = generate_suggestions(analysis)
    llm_review = get_llm_review(code, analysis)
    llm_review = clean_response(llm_review)
    formatted_review = format_review(llm_review)
    score = calculate_score(analysis)
    rating = classify_score(score)
    

    latest_report = {
        "analysis": analysis,
        "suggestions": suggestions,
        "llm_review": formatted_review,
        "score": score,
        "rating": rating
    }

    return render_template(
        'index.html',
        analysis=analysis,
        suggestions=suggestions,
        llm_review=formatted_review,
        score=score,
        rating=rating
    )


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    valid, status_message = validate_contact_form(name, email, message)
    if not valid:
        return render_template('index.html', contact_error=status_message, name=name, email=email, message=message)

    return render_template('index.html', contact_status=status_message)


@app.route('/download-report')
def download_report():
    generate_pdf(latest_report, "report.pdf")
    return send_file("report.pdf", as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)