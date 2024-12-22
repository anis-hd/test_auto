from flask import Flask, render_template_string
import json
import os

app = Flask(__name__)


# Load the JSON data when the app starts
def load_json():
    file_path = os.path.join(os.path.dirname(__file__), 'competency_tests.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        return f"Error loading JSON: {e}"


@app.route('/')
def index():
    # Load the JSON content
    data = load_json()

    if isinstance(data, str):
        return data  # If there's an error, return it as a message

    # Now parse the JSON data to generate HTML
    content = ""
    for key, value in data.items():
        content += f"<h2>{key}</h2>"
        content += f"<p>{value.replace('\n', '<br>')}</p>"

    # Basic HTML template to display the content
    html_content = f"""
    <html>
        <head><title>Competency Tests</title></head>
        <body>
            <h1>Competency Tests</h1>
            {content}
        </body>
    </html>
    """

    return render_template_string(html_content)


if __name__ == '__main__':
    app.run(debug=True)
