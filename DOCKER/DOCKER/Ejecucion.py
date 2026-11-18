from flask import Flask

app = Flask(__name__)

start = False

@app.route('/start', methods=['POST'])
def start_test():
    global start
    start = True
    return "OK"

@app.route('/status')
def status():
    return {"start": start}

app.run(host="0.0.0.0", port=5000)
