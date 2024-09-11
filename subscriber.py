from flask import Flask, request, jsonify, redirect
import subprocess
import threading

app = Flask(__name__)

messages = []

def subscribe_to_topic(host, port, topic):
    # Determine if TLS is needed based on the port
    if port == '8883':
        # Command to subscribe to a topic with TLS
        command = (
            f'mosquitto_sub -h {host} -p {port} -t {topic} '
            f'--cafile /home/mosquitto/certs/ca.crt '
            f'--tls-version tlsv1.2'
        )
    else:
        # Command to subscribe to a topic without TLS
        command = f'mosquitto_sub -h {host} -p {port} -t {topic}'
    
    # Run the subscription command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    # Read incoming messages
    for line in iter(process.stdout.readline, b''):
        messages.append(line.decode().strip())

@app.route('/subscribe', methods=['POST'])
def subscribe():
    host = request.form['host']
    port = request.form['port']
    topic = request.form['topic']

    # Start a new thread to handle the subscription
    threading.Thread(target=subscribe_to_topic, args=(host, port, topic)).start()

    return redirect('/')

@app.route('/get-messages')
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

