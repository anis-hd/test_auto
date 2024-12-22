import ollama
from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Function to prompt the user for competencies and difficulty
def get_user_input(competencies_str, difficulty_str):
    competencies = competencies_str.split(",")
    difficulty = difficulty_str.lower()
    return competencies, difficulty

# Function to generate tests using Ollama model
def generate_tests(competencies, difficulty, model='llama3.2:3b'):
    competency_tests = []

    for competency in competencies:
        competency = competency.strip()  # Clean up spaces
        question_to_ask = (
            f"Generate exactly 10 multiple-choice questions for the competency '{competency}' at a {difficulty} level. "
            f"The JSON response must contain exactly 10 objects, each representing a question. Each object should have: "
            f"'question' (string), 'choices' (list of strings), and 'correct_choice' (string). "
            f"Example JSON response format: "
            f'[{{"question": "What is 2+2?", "choices": ["1", "2", "4"], "correct_choice": "4"}}, ...]. '
            f"Do not include any extra text, explanations, or comments in the response."
            f"Make sure the response is in JSON format only, with no additional text or explanations. "
        )

        # Send the request to the Ollama model
        response = ollama.chat(model=model, messages=[{
            'role': 'user',
            'content': question_to_ask,
        }])

        try:
            # Parse the response content as JSON
            response_content = response.get('message', {}).get('content', '')
            test_data = json.loads(response_content)

            for test in test_data:
                competency_tests.append([
                    competency,
                    test.get('question', ''),
                    ", ".join(test.get('choices', [])),
                    test.get('correct_choice', '')
                ])
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error processing response for competency '{competency}': {e}")

    return competency_tests

# Route to render the input form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission and display the generated tests
@app.route('/generate_tests', methods=['POST'])
def generate_tests_view():
    competencies_str = request.form['competencies']
    difficulty_str = request.form['difficulty']

    # Get competencies and difficulty from the form
    competencies, difficulty = get_user_input(competencies_str, difficulty_str)

    # Generate tests for each competency
    competency_tests = generate_tests(competencies, difficulty)

    # Render the result as an HTML page with the test data
    return render_template('result.html', competency_tests=competency_tests)

if __name__ == "__main__":
    app.run(debug=True)
