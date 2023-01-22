from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

invites = {}

@app.route('/saveIP', methods=['GET'])
def save_ip():
    ip = request.args.get('IP')

    # Abre o arquivo de IPs e adiciona o novo IP
    with open("ips.txt", "a") as ips_file:
        ips_file.write(ip + "\n")
    response = 'IP Saved!'
    return (response)

@app.route('/checkIP', methods=['GET'])
def check_ip():
    ip = request.args.get('IP')
    with open("ips.txt", "r") as ips_file:
        if ip in ips_file.read().splitlines():
            response = "IP already exists"
            return (response)
        else:
            response = "IP not found"
            return (response)

@app.route('/')
def home():
    return 'never die'

@app.route('/inviteRegister')
def invite_count():
    id = request.args.get('id')

    if id in invites:
        invites[id] += 1
    else:
        invites[id] = 1

    response = jsonify({'userID': id,})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return (response)

@app.route('/inviteLog')
def invite_log():
    id = request.args.get('id')

    if id in invites:
        if invites[id] >= 20 and invites[id] < 50:
            tier_level = 1
        elif invites[id] >= 50 and invites[id] < 75:
            tier_level = 2
        elif invites[id] >= 75 and invites[id] < 110:
            tier_level = 3
        elif invites[id] >= 110:
            tier_level = 4
        else:
            tier_level = 0

        response = jsonify({'userID': id, 'invites': invites[id], 'tierLevel': tier_level})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return (response)
    else:
        response = jsonify({'userID': id, 'invites': 0, 'tierLevel': 0})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return (response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
