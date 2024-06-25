from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Starting HP for both player and enemy
player_hp = 10
enemy_hp = 10
player_points = 0

@app.route('/')
def survey():
    questions = [
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
    return render_template('survey.html', questions=questions)

@app.route('/results', methods=['POST'])
def results():
    responses = request.form
    profile_scores = {
        'Casual Gamer': 0,
        'Hardcore Gamer': 0,
        'Story-Driven Gamer': 0,
        'Competitive Gamer': 0,
        'Social Gamer': 0
    }
    
    # Scoring logic based on responses
    for question, answer in responses.items():
        if question == 'q1':
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

        if question == 'q2':
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

        if question == 'q3':
            if answer == 'Yes, I love playing with others.':
                profile_scores['Social Gamer'] += 2
                profile_scores['Competitive Gamer'] += 1
            elif answer == 'Occasionally, but I prefer single-player.':
                profile_scores['Story-Driven Gamer'] += 1
            elif answer == 'No, I prefer single-player experiences.':
                profile_scores['Story-Driven Gamer'] += 2

        if question == 'q4':
            if answer == 'Very important':
                profile_scores['Story-Driven Gamer'] += 2
            elif answer == 'Somewhat important':
                profile_scores['Casual Gamer'] += 1
            elif answer == 'Not important at all':
                profile_scores['Competitive Gamer'] += 1

        if question == 'q5':
            if answer == 'Yes, frequently':
                profile_scores['Social Gamer'] += 2
            elif answer == 'Sometimes':
                profile_scores['Social Gamer'] += 1
            elif answer == 'No, never':
                profile_scores['Casual Gamer'] += 1

    # Determine the profile with the highest score
    gamer_profile = max(profile_scores, key=profile_scores.get)
    return f"Your gamer profile is: {gamer_profile}"

@app.route('/interaction', methods=['GET', 'POST'])
def interaction():
    global player_hp, enemy_hp, player_points
    
    if request.method == 'POST':
        answer = request.form['answer']
        
        # Update HP based on answer chosen
        if answer == 'super_toxic':
            player_hp -= 2
        elif answer == 'toxic':
            player_hp -= 1
        elif answer == 'positive':
            enemy_hp -= 1
        elif answer == 'super_positive':
            enemy_hp -= 2
        elif answer == 'avoid_fight':
            player_points += 1
        
        # Ensure HP doesn't go below 0 or above 10
        player_hp = max(0, min(player_hp, 10))
        enemy_hp = max(0, min(enemy_hp, 10))
        
        # Check win/lose conditions
        if player_hp <= 0:
            return redirect(url_for('game_over'))
        elif enemy_hp <= 0:
            return redirect(url_for('congratulations'))
        elif player_points >= 3:
            return redirect(url_for('congratulations_bro'))
        
        # Redirect to interaction page to display updated HP
        return redirect(url_for('interaction'))
    
    return render_template('interaction.html', player_hp=player_hp, enemy_hp=enemy_hp)


@app.route('/game_over')
def game_over():
    return render_template('game_over.html')

@app.route('/congratulations')
def congratulations():
    return render_template('congratulations.html')

@app.route('/congratulations_bro')
def congratulations_bro():
    return render_template('congratulations_bro.html')

if __name__ == '__main__':
    app.run(debug=True)
