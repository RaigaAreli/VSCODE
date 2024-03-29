from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)

# Function that reads chat log from a given file path
def read_chat_log(file_path):
    try:
        with open(file_path, 'r') as file:
            chat_log = file.read()
        return chat_log
    except FileNotFoundError:
        return None

# Function to parse chat log and calculate participation grades
def calculate_participation_grades(chat_log):
    stud_answers = {}
    lines = chat_log.split('\n')  # Split chat log into lines
    
    for line in lines:
        if 'From' in line and 'To Everyone' in line:
            name = line.split('From ')[1].split(' To Everyone')[0]  # Get the name of the student
            answer = line.split(': ')[1].strip()  # Get the student's answer
            
            # Exclude teacher
            if name != 'Dr. Arnett Campbell':
                stud_answers.setdefault(name, 0)
                if answer:
                    if stud_answers[name] < 5:
                        stud_answers[name] += 1
    
    return stud_answers

# Function to calculate grade percentage
def calculate_grade_percentage(grade):
    return (grade / 5) * 100

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            chat_log_content = file.read().decode('utf-8')
            # Calculate participation grades
            participation_grades = calculate_participation_grades(chat_log_content)
            return render_template('results.html', participation_grades=participation_grades)
    return render_template('index.html', error='Please select a file.')

if __name__ == '__main__':
    app.run(debug=True)
