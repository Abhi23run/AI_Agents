from flask import Flask, request, jsonify

app = Flask(__name__)

def get_game_score(team_name):
    """Get the current score for a given NBA game"""
    team_name = team_name.lower()
    if "warriors" in team_name:
        return {"game_id": "401585601", "status": 'Final', "home_team": "Los Angeles Lakers", "home_team_score": 121, "away_team": "Golden State Warriors", "away_team_score": 128}
    elif "lakers" in team_name:
        return {"game_id": "401585601", "status": 'Final', "home_team": "Los Angeles Lakers", "home_team_score": 121, "away_team": "Golden State Warriors", "away_team_score": 128}
    elif "nuggets" in team_name:
        return {"game_id": "401585577", "status": 'Final', "home_team": "Miami Heat", "home_team_score": 88, "away_team": "Denver Nuggets", "away_team_score": 100}
    elif "heat" in team_name:
        return {"game_id": "401585577", "status": 'Final', "home_team": "Miami Heat", "home_team_score": 88, "away_team": "Denver Nuggets", "away_team_score": 100}
    else:
        return {"team_name": team_name, "score": "unknown"}

@app.route('/')
def home():
    """Root endpoint to guide users"""
    return '''
        <h1>Hi!</h1>
        <p>Welcome to the NBA Score API.</p>
        <p>Use the <code>/score</code> endpoint with a team name to get the latest game score.</p>
        <p>Example: <a href="/score?team=warriors">/score?team=warriors</a></p>
    '''

@app.route('/score', methods=['GET'])
def score():
    team_name = request.args.get('team', '')
    if not team_name:
        return jsonify({'error': 'Missing team name'}), 400
    score = get_game_score(team_name)
    return jsonify(score)

if __name__ == '__main__':
    app.run(debug=True)
