<!DOCTYPE html>
<html>
<head>
    <title>Teams to GitHub Webhook Receiver</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        .input-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"] { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #0078d4; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #106ebe; }
        .status { margin-top: 20px; padding: 10px; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Teams to GitHub Webhook Receiver</h1>
        
        <div class="input-group">
            <label for="githubToken">GitHub Personal Access Token:</label>
            <input type="text" id="githubToken" placeholder="ghp_xxxxxxxxxxxxxxxxxxxx">
        </div>
        
        <div class="input-group">
            <label for="repoOwner">GitHub Username:</label>
            <input type="text" id="repoOwner" placeholder="your-username">
        </div>
        
        <div class="input-group">
            <label for="repoName">Repository Name:</label>
            <input type="text" id="repoName" placeholder="teams-jira-webhook">
        </div>
        
        <div class="input-group">
            <label for="lambdaUrl">Lambda API Gateway URL:</label>
            <input type="text" id="lambdaUrl" placeholder="https://abc123def.execute-api.us-east-1.amazonaws.com/prod/webhook">
        </div>
        
        <button onclick="testConnection()">Test Connection</button>
        <button onclick="setupWebhook()">Setup Webhook</button>
        
        <div id="status"></div>
        
        <div class="info">
            <h3>Instructions:</h3>
            <ol>
                <li>Enter your GitHub token (create one at GitHub Settings → Developer settings → Personal access tokens)</li>
                <li>Enter your GitHub username and repository name</li>
                <li>Enter your Lambda API Gateway URL</li>
                <li>Click "Test Connection" to verify</li>
                <li>Click "Setup Webhook" to configure</li>
                <li>Post a message in Teams: <code>analyze XPR-10518</code></li>
            </ol>
        </div>
    </div>

    <script>
        async function testConnection() {
            const githubToken = document.getElementById('githubToken').value;
            const repoOwner = document.getElementById('repoOwner').value;
            const repoName = document.getElementById('repoName').value;
            const lambdaUrl = document.getElementById('lambdaUrl').value;
            const statusDiv = document.getElementById('status');
            
            if (!githubToken || !repoOwner || !repoName || !lambdaUrl) {
                statusDiv.innerHTML = '<div class="error">Please fill in all fields</div>';
                return;
            }
            
            try {
                // Test GitHub API access
                const response = await fetch(`https://api.github.com/repos/${repoOwner}/${repoName}`, {
                    headers: {
                        'Authorization': `token ${githubToken}`,
                        'Accept': 'application/vnd.github.v3+json'
                    }
                });
                
                if (response.ok) {
                    statusDiv.innerHTML = '<div class="success">✅ GitHub connection successful!</div>';
                } else {
                    statusDiv.innerHTML = '<div class="error">❌ GitHub connection failed: ' + response.statusText + '</div>';
                }
            } catch (error) {
                statusDiv.innerHTML = '<div class="error">❌ Error: ' + error.message + '</div>';
            }
        }
        
        async function setupWebhook() {
            const githubToken = document.getElementById('githubToken').value;
            const repoOwner = document.getElementById('repoOwner').value;
            const repoName = document.getElementById('repoName').value;
            const lambdaUrl = document.getElementById('lambdaUrl').value;
            const statusDiv = document.getElementById('status');
            
            if (!githubToken || !repoOwner || !repoName || !lambdaUrl) {
                statusDiv.innerHTML = '<div class="error">Please fill in all fields</div>';
                return;
            }
            
            try {
                // Create repository dispatch event
                const response = await fetch(`https://api.github.com/repos/${repoOwner}/${repoName}/dispatches`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `token ${githubToken}`,
                        'Accept': 'application/vnd.github.v3+json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        event_type: 'teams_message',
                        client_payload: {
                            message: 'analyze XPR-10518'
                        }
                    })
                });
                
                if (response.status === 204) {
                    statusDiv.innerHTML = '<div class="success">✅ Webhook setup successful! Test message sent to GitHub.</div>';
                } else {
                    statusDiv.innerHTML = '<div class="error">❌ Webhook setup failed: ' + response.statusText + '</div>';
                }
            } catch (error) {
                statusDiv.innerHTML = '<div class="error">❌ Error: ' + error.message + '</div>';
            }
        }
    </script>
</body>
</html>
