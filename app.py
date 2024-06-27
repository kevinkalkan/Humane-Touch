from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Starting HP for both player and enemy
player_hp = 10
enemy_hp = 10
player_points = 0

# Questions and answers for the battle
questions = [
    "Question 1: What's your favorite game and why?",
    "Question 2: How do you feel about game difficulty?",
    "Question 3: What's your opinion on multiplayer games?",
    "Question 4: What do you think about game graphics?",
    "Question 5: What's your view on game storytelling?",
    "Question 6: How do you choose which game to play next?",
    "Question 7: What do you think about game soundtracks?",
    "Question 8: How important is game replayability to you?",
    "Question 9: What's your favorite game genre?",
    "Question 10: How do you feel about game microtransactions?"
]
#super toxic-toxic-positive-super positive-avoid fight
answers = [
    ["You're clueless about games if you think that's the best. My little cousin could beat you.",
     "Seriously? Are you just trying to sound cool? Your taste in games is embarrassing.",
     "I appreciate games that challenge me and have deep stories. What's your favorite?",
     "I love how games can bring people together and create strong communities. It's incredible.",
     "Let's keep things civil. Everyone has their own preferences, right?"],
    ["That's way too easy. Are you a baby gamer?",
     "If you like easy games, you might as well watch a movie. No challenge at all.",
     "Challenging games are great, but accessibility matters too.",
     "A good balance between difficulty and fun is essential for a great game.",
     "Difficulty can be subjective. To each their own, I guess."],
    ["Multiplayer games are for people who can't handle real challenges.",
     "Multiplayer is overrated. Single-player is where the real skill is at.",
     "Multiplayer can be fun with friends and adds replayability.",
     "Multiplayer communities can create lasting friendships and great memories.",
     "Both modes have their own charm. It depends on what you're looking for."],
    ["Graphics don't matter if the game sucks. You're just being shallow.",
     "Good graphics can't save a bad game. You're just being a fanboy.",
     "Graphics enhance the experience but gameplay is the core.",
     "Stunning visuals can immerse you in the game's world.",
     "Graphics are just one aspect. Gameplay and story are equally important."],
    ["If you care so much about the story, go read a book.",
     "Storytelling is just an excuse for poor gameplay.",
     "A compelling story can make a good game great.",
     "Great storytelling can turn a game into a memorable experience.",
     "A good story can complement the gameplay, making it more engaging."],
    ["You must have no life to think so much about this.",
     "Choosing games? Just play whatever, doesn't matter.",
     "I look for recommendations and reviews before picking a game.",
     "I love exploring new games and genres. Keeps things fresh.",
     "It depends on my mood and what I'm interested in at the time."],
    ["Soundtracks? Really? Who even cares?",
     "Game music is just background noise. No big deal.",
     "A good soundtrack can elevate the gaming experience.",
     "Great music can make moments in games unforgettable.",
     "Soundtracks add to the atmosphere and immersion of the game."],
    ["Replayability is overrated. Just finish the game and move on.",
     "Who cares about replayability? One playthrough is enough.",
     "High replayability value keeps me coming back to a game.",
     "Games with replayability offer great value and longer enjoyment.",
     "Replayability can be a nice bonus, but it's not everything."],
    ["You must have terrible taste if that's your favorite genre.",
     "Seriously? That's your favorite? How basic.",
     "I enjoy a variety of genres depending on my mood.",
     "Every genre has its unique charm and strengths.",
     "Genres are just labels. A good game is a good game."],
    ["Microtransactions are the worst. They ruin games.",
     "If you like microtransactions, you must be a sucker.",
     "Microtransactions can be okay if done fairly.",
     "Games can stay relevant and funded through microtransactions.",
     "It's a mixed bag. Some implementations are better than others."]
]

current_question_index = 0
#Survey Questions and answers
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
    return redirect(url_for('analysing'))

@app.route('/interaction', methods=['GET', 'POST'])
def interaction():
    global player_hp, enemy_hp, player_points, current_question_index
    
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
        
        # Move to the next question
        current_question_index += 1
        if current_question_index >= len(questions):
            if player_hp > enemy_hp:
                return redirect(url_for('congratulations'))
            else:
                return redirect(url_for('game_over'))
        
        # Redirect back to interaction page
        return redirect(url_for('interaction'))
    
    return render_template('interaction.html', 
                           question=questions[current_question_index], 
                           answers=answers[current_question_index], 
                           player_hp=player_hp, 
                           enemy_hp=enemy_hp)

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

if __name__ == '__main__':
    app.run(debug=True)
