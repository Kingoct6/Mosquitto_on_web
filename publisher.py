from flask import Flask, request, redirect
import subprocess

app = Flask(__name__)

@app.route('/publish', methods=['POST'])
def publish():
    host = request.form['host']
    port = request.form['port']
    topic = request.form['topic']
    message = request.form['message']

    # Determine if TLS is needed based on the port
    if port == '8883':
        # Command to publish a message with TLS
        command = (
            f'mosquitto_pub -h {host} -p {port} -t {topic} -m "{message}" '
            f'--cafile /home/mosquitto/certs/ca.crt'
            f'--tls-version tlsv1.2'
        )
    else:
        # Command to publish a message without TLS
        command = f'mosquitto_pub -h {host} -p {port} -t {topic} -m "{message}"'
    
    # Run the command
    subprocess.run(command, shell=True)
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

