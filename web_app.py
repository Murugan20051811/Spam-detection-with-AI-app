"""
Insurance Spam Detection System - Flask Version
Runs on localhost with a web interface
"""

from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__)

# Groq API Configuration
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-8b-instant"

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insurance Spam Detection System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1f77e8 0%, #0056cc 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .input-section {
            margin-bottom: 30px;
        }
        
        .input-section h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        
        .input-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }
        
        input[type="text"],
        input[type="email"],
        textarea,
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="email"]:focus,
        textarea:focus,
        select:focus {
            outline: none;
            border-color: #1f77e8;
            box-shadow: 0 0 0 3px rgba(31, 119, 232, 0.1);
        }
        
        textarea {
            resize: vertical;
            min-height: 120px;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        button {
            flex: 1;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-analyze {
            background: linear-gradient(135deg, #1f77e8 0%, #0056cc 100%);
            color: white;
        }
        
        .btn-analyze:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(31, 119, 232, 0.4);
        }
        
        .btn-reset {
            background: #f0f0f0;
            color: #333;
        }
        
        .btn-reset:hover {
            background: #e0e0e0;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #1f77e8;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #1f77e8;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result-section {
            margin-top: 30px;
            display: none;
        }
        
        .result-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #1f77e8;
        }
        
        .result-card.spam {
            border-left-color: #e74c3c;
            background-color: #fee;
        }
        
        .result-card.safe {
            border-left-color: #27ae60;
            background-color: #efe;
        }
        
        .result-title {
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        .result-spam .result-title {
            color: #c0392b;
        }
        
        .result-safe .result-title {
            color: #1e8449;
        }
        
        .metric {
            display: inline-block;
            background: white;
            padding: 15px 20px;
            margin: 10px 10px 10px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .metric-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 1.5em;
            font-weight: 700;
            color: #1f77e8;
        }
        
        .reasons-list {
            margin-top: 15px;
        }
        
        .reasons-list h4 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .reasons-list li {
            margin-left: 20px;
            margin-bottom: 8px;
            color: #555;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #ddd;
        }
        
        .tab-btn {
            padding: 10px 20px;
            background: none;
            border: none;
            cursor: pointer;
            font-weight: 600;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }
        
        .tab-btn.active {
            color: #1f77e8;
            border-bottom-color: #1f77e8;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .error {
            background: #fee;
            color: #c0392b;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Insurance Spam Detection System</h1>
            <p>AI-Powered Protection Against Insurance Fraud & Spam</p>
        </div>
        
        <div class="content">
            <div class="input-section">
                <h2>Analyze Content</h2>
                
                <div style="margin-bottom: 20px;">
                    <div class="tabs">
                        <button class="tab-btn active" onclick="switchTab('email')">📧 Email</button>
                        <button class="tab-btn" onclick="switchTab('sms')">💬 SMS</button>
                        <button class="tab-btn" onclick="switchTab('phone')">☎️ Phone</button>
                        <button class="tab-btn" onclick="switchTab('text')">✍️ Text</button>
                    </div>
                </div>
                
                <!-- Email Tab -->
                <div id="email" class="tab-content active">
                    <div class="input-group">
                        <label>Sender Email Address</label>
                        <input type="email" id="senderEmail" placeholder="sender@example.com">
                    </div>
                    <div class="input-group">
                        <label>Email Subject</label>
                        <input type="text" id="emailSubject" placeholder="Email subject line">
                    </div>
                    <div class="input-group">
                        <label>Email Body</label>
                        <textarea id="emailBody" placeholder="Paste email content here..."></textarea>
                    </div>
                </div>
                
                <!-- SMS Tab -->
                <div id="sms" class="tab-content">
                    <div class="input-group">
                        <label>Sender Phone Number</label>
                        <input type="text" id="senderPhone" placeholder="+1-123-456-7890">
                    </div>
                    <div class="input-group">
                        <label>Message Content</label>
                        <textarea id="smsMessage" placeholder="Paste SMS content here..."></textarea>
                    </div>
                </div>
                
                <!-- Phone Tab -->
                <div id="phone" class="tab-content">
                    <div class="input-group">
                        <label>Phone Number</label>
                        <input type="text" id="phoneNumber" placeholder="+1-123-456-7890">
                    </div>
                    <div class="input-group">
                        <label>Context (optional)</label>
                        <textarea id="phoneContext" placeholder="Where/how did you receive this number?"></textarea>
                    </div>
                </div>
                
                <!-- Text Tab -->
                <div id="text" class="tab-content">
                    <div class="input-group">
                        <label>Text Content</label>
                        <textarea id="generalText" placeholder="Paste any text for spam analysis..."></textarea>
                    </div>
                </div>
                
                <div class="button-group">
                    <button class="btn-analyze" onclick="analyzeContent()">🔍 Analyze</button>
                    <button class="btn-reset" onclick="resetForm()">🔄 Reset</button>
                </div>
                
                <div class="error" id="errorMsg"></div>
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyzing with AI...</p>
                </div>
            </div>
            
            <div class="result-section" id="resultSection">
                <div id="resultContent"></div>
            </div>
        </div>
        
        <div class="footer">
            <p>🤖 Powered by Groq - Llama 3.1 8B Instant | 🔐 Privacy-Focused | ⚡ Real-Time Analysis</p>
        </div>
    </div>
    
    <script>
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
            });
            document.querySelectorAll('.tab-btn').forEach(el => {
                el.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        function analyzeContent() {
            const activeTab = getActiveTab();
            let content = '';
            let type = '';
            
            if (activeTab === 'email') {
                const email = document.getElementById('senderEmail').value;
                const subject = document.getElementById('emailSubject').value;
                const body = document.getElementById('emailBody').value;
                
                if (!email || !subject || !body) {
                    showError('Please fill all email fields');
                    return;
                }
                content = `From: ${email}\nSubject: ${subject}\n\nBody:\n${body}`;
                type = 'email';
            } else if (activeTab === 'sms') {
                const phone = document.getElementById('senderPhone').value;
                const message = document.getElementById('smsMessage').value;
                
                if (!phone || !message) {
                    showError('Please fill all SMS fields');
                    return;
                }
                content = `From: ${phone}\n\nMessage:\n${message}`;
                type = 'SMS';
            } else if (activeTab === 'phone') {
                const phone = document.getElementById('phoneNumber').value;
                const context = document.getElementById('phoneContext').value;
                
                if (!phone) {
                    showError('Please enter a phone number');
                    return;
                }
                content = `Phone: ${phone}\nContext: ${context || 'No context provided'}`;
                type = 'phone number';
            } else {
                const text = document.getElementById('generalText').value;
                
                if (!text) {
                    showError('Please enter text content');
                    return;
                }
                content = text;
                type = 'text';
            }
            
            hideError();
            showLoading();
            
            fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: content,
                    type: type
                })
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                displayResults(data);
            })
            .catch(error => {
                hideLoading();
                showError('Error analyzing content: ' + error);
            });
        }
        
        function displayResults(data) {
            const resultSection = document.getElementById('resultSection');
            const resultContent = document.getElementById('resultContent');
            
            if (data.error) {
                resultContent.innerHTML = `<div class="result-card"><p style="color: #c0392b;">${data.error}</p></div>`;
                resultSection.style.display = 'block';
                return;
            }
            
            const isSpam = data.is_spam;
            const confidence = data.confidence || 0;
            const riskLevel = data.risk_level || 'unknown';
            const reasons = data.reasons || [];
            const recommendation = data.recommendation || '';
            
            let html = `<div class="result-card ${isSpam ? 'spam' : 'safe'}">`;
            html += `<div class="result-title">${isSpam ? '🚨 SPAM DETECTED' : '✅ LEGITIMATE'}</div>`;
            html += `<div>`;
            html += `<div class="metric"><div class="metric-label">Confidence</div><div class="metric-value">${confidence}%</div></div>`;
            html += `<div class="metric"><div class="metric-label">Risk Level</div><div class="metric-value">${riskLevel.toUpperCase()}</div></div>`;
            html += `</div>`;
            
            if (reasons.length > 0) {
                html += `<div class="reasons-list"><h4>Detected Issues:</h4><ul>`;
                reasons.forEach(reason => {
                    html += `<li>${reason}</li>`;
                });
                html += `</ul></div>`;
            }
            
            if (recommendation) {
                html += `<div style="margin-top: 15px; padding: 15px; background: white; border-radius: 8px;"><strong>💡 Recommendation:</strong> ${recommendation}</div>`;
            }
            
            html += `</div>`;
            
            resultContent.innerHTML = html;
            resultSection.style.display = 'block';
        }
        
        function getActiveTab() {
            const tabs = document.querySelectorAll('.tab-content');
            for (let tab of tabs) {
                if (tab.classList.contains('active')) {
                    return tab.id;
                }
            }
            return 'email';
        }
        
        function resetForm() {
            document.querySelectorAll('input[type="text"], input[type="email"], textarea').forEach(el => {
                el.value = '';
            });
            document.getElementById('resultSection').style.display = 'none';
            hideError();
        }
        
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
        }
        
        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }
        
        function showError(msg) {
            const errorDiv = document.getElementById('errorMsg');
            errorDiv.textContent = msg;
            errorDiv.style.display = 'block';
        }
        
        function hideError() {
            document.getElementById('errorMsg').style.display = 'none';
        }
    </script>
</body>
</html>
"""

def detect_spam_with_groq(content, content_type):
    """Detect spam using Groq API"""
    try:
        prompt = f"""You are an advanced spam detection system specialized in insurance fraud and spam detection.

Analyze the following {content_type} for spam characteristics:

Content:
{content}

Evaluate for:
1. Spam indicators (unsolicited promotions, suspicious offers, etc.)
2. Phishing attempts
3. Insurance fraud indicators
4. Urgency tactics
5. Requests for personal/financial information

Respond in JSON format with:
- "is_spam": true/false
- "confidence": 0-100
- "risk_level": "high", "medium", "low"
- "reasons": [list of detected issues]
- "recommendation": brief advice

RESPOND ONLY WITH VALID JSON."""

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 1024
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            response_text = result["choices"][0]["message"]["content"]
            try:
                analysis = json.loads(response_text)
                return analysis
            except json.JSONDecodeError:
                return {
                    "is_spam": True,
                    "confidence": 50,
                    "risk_level": "medium",
                    "reasons": ["Unable to parse analysis"],
                    "recommendation": "Please review content manually"
                }
        return None
            
    except Exception as e:
        return {
            "error": f"API Error: {str(e)}",
            "recommendation": "Please try again later"
        }

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    content = data.get('content', '')
    content_type = data.get('type', 'text')
    
    if not content:
        return jsonify({"error": "No content provided"})
    
    analysis = detect_spam_with_groq(content, content_type)
    return jsonify(analysis or {"error": "Analysis failed"})

if __name__ == '__main__':
    print("🚀 Insurance Spam Detection System Starting...")
    print("📍 Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=False, port=5000, host='127.0.0.1')
