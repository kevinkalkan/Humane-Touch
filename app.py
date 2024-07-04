from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load interaction questions and answers from JSON file
with open('questions.json') as f:
    interaction_data = json.load(f)
    interaction_questions = interaction_data['questions']
    interaction_answers = interaction_data['answers']

# Survey Questions and answers
survey_questions = [
    {
        'id': 'q1',
        'question': 'How often do you play video games?',
        'answers': ['Daily', 'Weekly', 'Monthly', 'Rarely']
    },
    {
        'id': 'q2',
        'question': 'What type of games do you prefer?',
        'answers': ['Action/Adventure', 'Role-Playing Games (RPGs)', 'First-Person Shooters (FPS)', 'Sports', 'Puzzle']
    },
    {
        'id': 'q3',
        'question': 'Do you enjoy multiplayer games?',
        'answers': ['Yes, I love playing with others.', 'Occasionally, but I prefer single-player.', 'No, I prefer single-player experiences.']
    },
    {
        'id': 'q4',
        'question': 'How important is the story in a game to you?',
        'answers': ['Very important', 'Somewhat important', 'Not important at all']
    },
    {
        'id': 'q5',
        'question': 'Do you participate in gaming communities or forums?',
        'answers': ['Yes, frequently', 'Sometimes', 'No, never']
    }
]

# Load replies from JSON file
with open('replies.json') as f:
    replies = json.load(f)

# Reset HP and points function
def reset_hp_points():
    session['player_hp'] = 10
    session['enemy_hp'] = 10
    session['player_points'] = 0
    session['current_question_index'] = 0

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    # Initialize session variables if they don't exist
    if 'responses' not in session:
        session['responses'] = []
    if 'current_question_index' not in session:
        session['current_question_index'] = 0

    current_question_index = session['current_question_index']

    if request.method == 'POST':
        selected_answers = request.form.getlist('answers')
        if not selected_answers:
            error = "Please select at least one answer."
            return render_template('survey.html', question=survey_questions[current_question_index], error=error)
        
        session['responses'].append(selected_answers)
        session['current_question_index'] += 1

        if current_question_index >= len(survey_questions):
            return redirect(url_for('analysing'))
        
        return redirect(url_for('survey'))

    if current_question_index >= len(survey_questions):
        return redirect(url_for('analysing'))

    return render_template('survey.html', question=survey_questions[current_question_index])

@app.route('/results', methods=['POST'])
def results():
    responses = session.get('responses', [])
    profile_scores = {
        'Casual Gamer': 0,
        'Hardcore Gamer': 0,
        'Story-Driven Gamer': 0,
        'Competitive Gamer': 0,
        'Social Gamer': 0
    }
    
    # Scoring logic based on responses
    for question, answers in zip(survey_questions, responses):
        answer = answers[0]  # Assuming only one answer per question for simplicity
        if question['id'] == 'q1':
            if answer == 'Daily':
                profile_scores['Hardcore Gamer'] += 2
                profile_scores['Competitive Gamer'] += 1
            elif answer == 'Weekly':
                profile_scores['Casual Gamer'] += 1
                profile_scores['Story-Driven Gamer'] += 1
            elif answer == 'Monthly':
                profile_scores['Casual Gamer'] += 2
            elif answer == 'Rarely':
                profile_scores['Casual Gamer'] += 3

        if question['id'] == 'q2':
            if answer == 'Action/Adventure':
                profile_scores['Story-Driven Gamer'] += 2
            elif answer == 'Role-Playing Games (RPGs)':
                profile_scores['Story-Driven Gamer'] += 2
            elif answer == 'First-Person Shooters (FPS)':
                profile_scores['Competitive Gamer'] += 2
            elif answer == 'Sports':
                profile_scores['Casual Gamer'] += 1
                profile_scores['Competitive Gamer'] += 1
            elif answer == 'Puzzle':
                profile_scores['Casual Gamer'] += 2

        if question['id'] == 'q3':
            if answer == 'Yes, I love playing with others.':
                profile_scores['Social Gamer'] += 2
                profile_scores['Competitive Gamer'] += 1
            elif answer == 'Occasionally, but I prefer single-player.':
                profile_scores['Story-Driven Gamer'] += 1
            elif answer == 'No, I prefer single-player experiences.':
                profile_scores['Story-Driven Gamer'] += 2

        if question['id'] == 'q4':
            if answer == 'Very important':
                profile_scores['Story-Driven Gamer'] += 2
            elif answer == 'Somewhat important':
                profile_scores['Casual Gamer'] += 1
            elif answer == 'Not important at all':
                profile_scores['Competitive Gamer'] += 1

        if question['id'] == 'q5':
            if answer == 'Yes, frequently':
                profile_scores['Social Gamer'] += 2
            elif answer == 'Sometimes':
                profile_scores['Social Gamer'] += 1
            elif answer == 'No, never':
                profile_scores['Casual Gamer'] += 1

    # Determine the profile with the highest score
    gamer_profile = max(profile_scores, key=profile_scores.get)
    return redirect(url_for('analysing'))

@app.route('/interaction')
def interaction():
    reset_hp_points()
    return render_template('interaction.html', 
                           question=interaction_questions[session['current_question_index']], 
                           answers=interaction_answers[session['current_question_index']], 
                           player_hp=session['player_hp'], 
                           enemy_hp=session['enemy_hp'],
                           player_points=session['player_points'])

@app.route('/interaction', methods=['POST'])
def interaction_post():
    answer = request.form['answer']
    
    # Update HP and points based on answer chosen
    if answer == 'super_toxic':
        session['player_hp'] -= 2
    elif answer == 'toxic':
        session['player_hp'] -= 1
    elif answer == 'positive':
        session['enemy_hp'] -= 1
    elif answer == 'super_positive':
        session['enemy_hp'] -= 2
    elif answer == 'avoid_fight':
        session['player_points'] += 1
    
    # Ensure HP doesn't go below 0 or above 10
    session['player_hp'] = max(0, min(session['player_hp'], 10))
    session['enemy_hp'] = max(0, min(session['enemy_hp'], 10))
    
    # Get random reply based on answer
    if answer in replies:
        random_reply = random.choice(replies[answer])
    else:
        random_reply = "Interesting choice!"

    # Check win/lose conditions
    if session['player_hp'] <= 0:
        return redirect(url_for('game_over'))
    elif session['enemy_hp'] <= 0:
        return redirect(url_for('congratulations'))
    elif session['player_points'] >= 3:
        return redirect(url_for('congratulations_bro'))
    
    # Move to the next question
    session['current_question_index'] += 1
    if session['current_question_index'] >= len(interaction_questions):
        if session['player_hp'] > session['enemy_hp']:
            return redirect(url_for('congratulations'))
        else:
            return redirect(url_for('game_over'))
    
    return render_template('interaction.html', 
                           question=interaction_questions[session['current_question_index']], 
                           answers=interaction_answers[session['current_question_index']], 
                           player_hp=session['player_hp'], 
                           enemy_hp=session['enemy_hp'],
                           player_points=session['player_points'],
                           random_reply=random_reply)

@app.route('/game_over')
def game_over():
    return render_template('game_over.html')

@app.route('/congratulations')
def congratulations():
    return render_template('congratulations.html')

@app.route('/congratulations_bro')
def congratulations_bro():
    return render_template('congratulations_bro.html')

@app.route('/analysing')
def analysing():
    return render_template('analysing.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
