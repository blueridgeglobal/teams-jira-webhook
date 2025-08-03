from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get the message from Teams
        data = request.json
        message = data.get('text', '')
        
        # Trigger GitHub Actions workflow
        github_token = os.getenv('GITHUB_TOKEN')
        repo_owner = 'YOUR_GITHUB_USERNAME'  # Replace with your GitHub username
        repo_name = 'teams-jira-webhook'
        
        # Create repository dispatch event
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/dispatches'
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        payload = {
            'event_type': 'teams_message',
            'client_payload': {
                'message': message
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 204:
            return jsonify({'status': 'success', 'message': 'Message forwarded to Lambda'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to forward message'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
