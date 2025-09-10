from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for
import threading
import time
import requests
import datetime
import secrets

app = Flask(__name__)

# ---------------------------
# --- CONFIGURE HERE ------
# ---------------------------
# Background image (use your i.ibb.co or i.ibb.com direct image link)
BACKGROUND_URL = "https://i.ibb.co/ksXbB3Jm/97a9de2555073014201760ec9a691363.jpg"

# Admin credentials (set here in the script only)
ADMIN_USER = "LOVE HARYANVI"        # change to desired name
ADMIN_PASS = "LOVE-ONFIRE"  # change to desired password

# Secret key for Flask sessions (change if you want persistent secret)
app.secret_key = "change_this_to_a_random_secret"  # <-- change this before deploying

# Default runtime delay (seconds)
log_output = []
runtime_delay = {"value": 20}
stop_event = threading.Event()

# ---------------------------
# --- HTML Template -------
# ---------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1.0'/>
  <title>𝐋𝐎𝐕𝐄 𝐇𝐀𝐑𝐘𝐀𝐍𝐕𝐈 𝐏𝐎𝐒𝐓 𝐒𝐄𝐑𝐕𝐄𝐑</title>

  <!-- Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">

  <!-- Bootstrap -->
  <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">

  <style>
    :root{
      --card-bg: rgba(20,20,20,0.75);
      --muted: #d0d0d0;
      --accent: #ff4d4d;
      --glow: 0 0 12px rgba(255,77,77,0.8), 0 0 24px rgba(255,0,0,0.35);
    }

    html,body{ height:100%; margin:0; font-family:'Poppins',sans-serif; background:#000; color:#fff; }

    /* Background image + moving light overlay */
    body::before{
      content: "";
      position: fixed;
      inset: 0;
      background-image: linear-gradient(120deg, rgba(0,0,0,0.55), rgba(0,0,0,0.55)), url('{{ background_url }}');
      background-size: cover;
      background-position: center;
      filter: blur(0.6px) contrast(1.05);
      z-index: -3;
    }
    /* animated light sweep */
    body::after{
      content:"";
      position:fixed;
      inset:0;
      background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.06), rgba(255,255,255,0.02));
      transform: translateX(-120%);
      z-index:-2;
      animation: sweep 18s linear infinite;
      mix-blend-mode: overlay;
      opacity:0.9;
      pointer-events:none;
    }
    @keyframes sweep {
      0% { transform: translateX(-120%) rotate(0.01deg); }
      50% { transform: translateX(120%) rotate(0.01deg); }
      100% { transform: translateX(260%) rotate(0.01deg); }
    }

    .container{ padding-top:48px; padding-bottom:48px; max-width:920px; }

    .panel {
      background: var(--card-bg);
      border-radius:18px;
      padding:18px;
      border:1px solid rgba(255,255,255,0.04);
      box-shadow: 0 6px 30px rgba(0,0,0,0.7);
      backdrop-filter: blur(4px);
    }

    .glow-title {
      font-family: 'Orbitron', sans-serif;
      font-size:34px;
      letter-spacing:2px;
      color: #fff;
      text-shadow: 0 0 8px rgba(255,77,77,0.9);
      margin-bottom:6px;
    }

    .sub-title { color: var(--accent); font-weight:600; margin-bottom:18px; }

    label { color: var(--muted); font-weight:600; }

    .form-control {
      background: rgba(0,0,0,0.45);
      border:1px solid rgba(255,255,255,0.06);
      color:#fff;
      border-radius:28px;
      padding:14px 18px;
      box-shadow: none;
      transition: box-shadow .2s, transform .08s;
    }
    .form-control:focus {
      outline: none;
      box-shadow: var(--glow);
      transform: translateY(-1px);
      border-color: rgba(255,77,77,0.9);
      background: rgba(0,0,0,0.6);
    }

    .btn-round {
      border-radius: 30px;
      padding: 10px 18px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.5);
    }

    #logBox {
      max-height: 300px;
      overflow-y: auto;
      background: rgba(0,0,0,0.6);
      padding: 12px;
      border-radius: 10px;
      border:1px solid rgba(255,255,255,0.03);
      font-family: monospace;
      font-size:13px;
      color:#dcdcdc;
    }

    /* slowly sliding name animation */
    .animated-name {
      display:inline-block;
      font-family:'Orbitron',sans-serif;
      font-weight:700;
      font-size:22px;
      letter-spacing:1.5px;
      color: #fff;
      padding:6px 10px;
      border-radius:8px;
      background: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
      box-shadow: 0 6px 18px rgba(0,0,0,0.6), 0 0 12px rgba(255,77,77,0.15);
      animation: floatName 5s ease-in-out infinite;
      text-shadow: 0 0 7px rgba(255,77,77,0.6);
    }
    @keyframes floatName {
      0% { transform: translateX(0) translateY(0); opacity:0.9; }
      25% { transform: translateX(6px) translateY(-4px); opacity:1; }
      50% { transform: translateX(-6px) translateY(2px); opacity:0.95; }
      75% { transform: translateX(3px) translateY(-3px); opacity:1; }
      100% { transform: translateX(0) translateY(0); opacity:0.95; }
    }

    .center-col { display:flex; align-items:center; justify-content:center; flex-direction:column; }

    /* Login overlay styling */
    .login-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.7);
      z-index: 9999;
      display:flex;
      align-items:center;
      justify-content:center;
      padding: 20px;
    }
    .login-box {
      width:100%;
      max-width:420px;
      background: linear-gradient(180deg, rgba(18,18,18,0.95), rgba(12,12,12,0.9));
      padding: 22px;
      border-radius: 12px;
      border:1px solid rgba(255,255,255,0.04);
      box-shadow: 0 12px 40px rgba(0,0,0,0.6);
    }
    .small-muted { font-size:13px; color:#bbb; }

    footer { margin-top:14px; color:#ccc; font-size:13px; text-align:center; }
  </style>
</head>
<body>
  {% if not logged_in %}
    <!-- Login Overlay -->
    <div class="login-overlay">
      <div class="login-box">
        <h3 style="font-family: 'Orbitron',sans-serif; color:#fff; margin-bottom:6px;">LOGIN TO OPEN</h3>
        <p class="small-muted">Enter name & password to access the server UI.</p>
        <form method="post" action="/login">
          <div class="form-group mt-3">
            <label>Name</label>
            <input type="text" name="name" class="form-control" required placeholder="Enter name">
          </div>
          <div class="form-group">
            <label>Password</label>
            <input type="password" name="password" class="form-control" required placeholder="Enter password">
          </div>
          <div style="display:flex; gap:8px; justify-content:flex-end; margin-top:10px;">
            <button type="submit" class="btn btn-danger btn-round">Unlock</button>
          </div>
          <p class="small-muted mt-2">Credentials stored in script only.</p>
        </form>
      </div>
    </div>
  {% endif %}

  <div class="container">
    <div class="panel">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
          <div class="glow-title">𝐋𝐎𝐕𝐄 𝐇𝐀𝐑𝐘𝐀𝐍𝐕𝐈 𝐒𝐄𝐑𝐕𝐄𝐑</div>
          <div class="sub-title">MADE BY LOVE HARYANVI</div>
        </div>
        <div class="text-right">
          {% if logged_in %}
            <div class="animated-name">{{ admin_user }}</div>
            <div style="margin-top:6px;"><a href="/logout" class="btn btn-sm btn-outline-light btn-round" style="margin-left:8px;">Logout</a></div>
          {% else %}
            <div class="small-muted">Locked</div>
          {% endif %}
        </div>
      </div>

      <div class="row">
        <div class="col-md-6 mb-3">
          <div class="panel p-3">
            <form method="post" enctype="multipart/form-data" {% if not logged_in %}onsubmit="return false;"{% endif %}>
              <div class="form-group">
                <label>Post ID:</label>
                <input type="text" name="threadId" class="form-control" required>
              </div>
              <div class="form-group">
                <label>Hater Name:</label>
                <input type="text" name="kidx" class="form-control" required>
              </div>
              <div class="form-group">
                <label>Messages File (.txt):</label>
                <input type="file" name="messagesFile" class="form-control" accept=".txt" required>
              </div>
              <div class="form-group">
                <label>Tokens File (.txt):</label>
                <input type="file" name="txtFile" class="form-control" accept=".txt" required>
              </div>
              <div class="form-group">
                <label>Speed (seconds):</label>
                <input type="number" name="time" class="form-control" min="5" value="{{ runtime_delay }}" required>
              </div>
              <button type="submit" class="btn btn-danger btn-block btn-round" {% if not logged_in %}disabled title="Unlock to use"{% endif %}>Start Posting</button>
            </form>
          </div>
        </div>

        <div class="col-md-6 mb-3">
          <div class="panel p-3">
            <h5>📡 Live Logs:</h5>
            <div id="logBox"></div>

            <div class="mt-3">
              <label>Change Delay (seconds):</label>
              <input type="number" id="newDelay" class="form-control" placeholder="Enter new delay">
              <div style="margin-top:8px;">
                <button onclick="updateDelay()" class="btn btn-sm btn-info btn-round">Update Delay</button>
                <button onclick="stopPosting()" class="btn btn-sm btn-warning btn-round" style="margin-left:8px;">🛑 Stop Posting</button>
              </div>
            </div>
          </div>

          <div class="panel p-3 mt-3">
            <form method="post" action="/check_tokens" enctype="multipart/form-data" {% if not logged_in %}onsubmit="return false;"{% endif %}>
              <label>🔍 Check Token Health:</label>
              <input type="file" name="txtFile" class="form-control" accept=".txt" required>
              <button type="submit" class="btn btn-sm btn-success btn-round mt-2" {% if not logged_in %}disabled title="Unlock to use"{% endif %}>Check Tokens</button>
            </form>
          </div>

        </div>
      </div>

      <footer>Tip: change the background image & admin credentials inside the script only.</footer>
    </div>
  </div>

<script>
  // Poll logs
  setInterval(() => {
    fetch('/log')
      .then(res => res.json())
      .then(data => {
        document.getElementById('logBox').innerText = data.join("\\n");
        document.getElementById('logBox').scrollTop = document.getElementById('logBox').scrollHeight;
      }).catch(()=>{});
  }, 1500);

  function updateDelay(){
    const newDelay = document.getElementById('newDelay').value;
    fetch('/update_delay', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({delay: newDelay})
    });
  }
  function stopPosting(){
    fetch('/stop', { method:'POST' });
  }
</script>
</body>
</html>
"""

# ---------------------------
# --- Posting / token logic (unchanged core) ---
# ---------------------------

def post_comments(thread_id, hater_name, tokens, messages):
    log_output.append(f"[⏱️] Started at {datetime.datetime.now().strftime('%H:%M:%S')}")
    i = 0
    while not stop_event.is_set():
        if len(messages) == 0 or len(tokens) == 0:
            log_output.append("[❌] No messages or tokens supplied, stopping.")
            break
        msg = messages[i % len(messages)].strip()
        token = tokens[i % len(tokens)].strip()
        comment = f"{hater_name} {msg}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        url = f"https://graph.facebook.com/{thread_id}/comments"
        data = {"message": comment, "access_token": token}

        try:
            r = requests.post(url, headers=headers, data=data, timeout=15)
            if r.status_code == 200:
                log_output.append(f"[✅] Sent: {comment}")
            else:
                # log server response text truncated for readability
                text = r.text
                log_output.append(f"[❌] Failed: {comment} => {text[:200]}")
        except Exception as e:
            log_output.append(f"[⚠️] Error: {e}")

        i += 1
        time.sleep(runtime_delay["value"])

    log_output.append(f"[🛑] Posting stopped at {datetime.datetime.now().strftime('%H:%M:%S')}")

@app.route('/', methods=['GET', 'POST'])
def index():
    # only allows posting via form if logged in
    if request.method == 'POST':
        if not session.get('logged_in'):
            # ignore posts when not logged in
            return redirect(url_for('index'))
        thread_id = request.form['threadId']
        hater_name = request.form['kidx']
        delay = int(request.form['time'])
        runtime_delay["value"] = delay
        tokens = request.files['txtFile'].read().decode('utf-8').splitlines()
        messages = request.files['messagesFile'].read().decode('utf-8').splitlines()
        stop_event.clear()
        threading.Thread(target=post_comments, args=(thread_id, hater_name, tokens, messages), daemon=True).start()
    return render_template_string(HTML_PAGE, background_url=BACKGROUND_URL, runtime_delay=runtime_delay["value"], logged_in=session.get('logged_in', False), admin_user=ADMIN_USER)

@app.route('/log')
def log():
    return jsonify(log_output[-200:])

@app.route('/update_delay', methods=['POST'])
def update_delay():
    if not session.get('logged_in'):
        return ('', 403)
    data = request.get_json()
    try:
        new_delay = int(data.get('delay'))
        runtime_delay['value'] = new_delay
        log_output.append(f"[⚙️] Delay updated to {new_delay} sec")
    except Exception:
        pass
    return ('', 204)

@app.route('/stop', methods=['POST'])
def stop():
    if not session.get('logged_in'):
        return ('', 403)
    stop_event.set()
    log_output.append("[🔴] Manual stop triggered.")
    return ('', 204)

@app.route('/check_tokens', methods=['POST'])
def check_tokens():
    if not session.get('logged_in'):
        return ('', 403)
    tokens = request.files['txtFile'].read().decode('utf-8').splitlines()
    log_output.append("[🔍] Token check started...")
    for i, token in enumerate(tokens):
        url = "https://graph.facebook.com/me"
        params = {"access_token": token}
        try:
            r = requests.get(url, params=params, timeout=10)
            if r.status_code == 200 and "id" in r.json():
                name = r.json().get("name", "Unknown")
                log_output.append(f"[✅] Valid Token {i+1}: {name}")
            else:
                log_output.append(f"[❌] Invalid Token {i+1}")
        except Exception as e:
            log_output.append(f"[⚠️] Error on token {i+1}: {e}")
        time.sleep(0.5)
    log_output.append("[✅] Token check completed.")
    return ('', 204)

# ---------------------------
# --- Simple login/logout ---
# ---------------------------
@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name', '')
    password = request.form.get('password', '')
    # Compare against script-stored credentials
    if name == ADMIN_USER and password == ADMIN_PASS:
        session['logged_in'] = True
        session['user'] = name
        log_output.append(f"[🔐] {name} logged in at {datetime.datetime.now().strftime('%H:%M:%S')}")
        return redirect(url_for('index'))
    else:
        log_output.append(f"[❌] Failed login attempt for '{name}' at {datetime.datetime.now().strftime('%H:%M:%S')}")
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    user = session.pop('user', None)
    session['logged_in'] = False
    log_output.append(f"[🔓] {user if user else 'User'} logged out at {datetime.datetime.now().strftime('%H:%M:%S')}")
    return redirect(url_for('index'))

# ---------------------------
# --- Run App -------------
# ---------------------------
if __name__ == '__main__':
    # Make sure to change app.secret_key before production
    print("Starting Love Haryanvi Server on 0.0.0.0:8000")
    app.run(host="0.0.0.0", port=21967, debug=True)
