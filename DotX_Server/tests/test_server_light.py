from flask import Flask, jsonify
import time

app = Flask(__name__)

# Biến lưu trạng thái của đèn
lights_state = {
    "light1": "off",  # Đèn trắng
    "light2": "off"   # Đèn vàng
}

# API bật đèn 1 (trắng)
@app.route('/light1/on', methods=['GET'])
def light1_on():
    lights_state["light1"] = "on"
    print("Đèn trắng đã được bật.")
    return jsonify({"message": "Đèn trắng đã được bật."})

# API tắt đèn 1 (trắng)
@app.route('/light1/off', methods=['GET'])
def light1_off():
    lights_state["light1"] = "off"
    print("Đèn trắng đã được tắt.")
    return jsonify({"message": "Đèn trắng đã được tắt."})

# API bật đèn 2 (vàng)
@app.route('/light2/on', methods=['GET'])
def light2_on():
    lights_state["light2"] = "on"
    print("Đèn vàng đã được bật.")
    return jsonify({"message": "Đèn vàng đã được bật."})

# API tắt đèn 2 (vàng)
@app.route('/light2/off', methods=['GET'])
def light2_off():
    lights_state["light2"] = "off"
    print("Đèn vàng đã được tắt.")
    return jsonify({"message": "Đèn vàng đã được tắt."})

# API bật đèn 1 (trắng) và đèn 2 (vàng)
@app.route('/light1andlight2/on', methods=['GET'])
def light1andlight2_on():
    lights_state["light1"] = "on"
    print("Cả 2 đèn đã được bật.")
    return jsonify({"message": "Cả 2 đèn đã được bật."})

# API tắt đèn 1 (trắng) và đèn 2 (vàng)
@app.route('/light1andlight2/off', methods=['GET'])
def light1andlight2_off():
    lights_state["light1"] = "off"
    print("Cả 2 đèn đã được tắt.")
    return jsonify({"message": "Cả 2 đèn đã được tắt."})

# API kiểm tra trạng thái các đèn
@app.route('/status', methods=['GET'])
def status():
    return jsonify(lights_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Chạy server trên tất cả các địa chỉ IP và port 5000
