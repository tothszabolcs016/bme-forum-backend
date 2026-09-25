from flask import Flask, request, jsonify
from data_manager import JsonDataManager
import os

app = Flask(__name__)
db = JsonDataManager()

@app.route('/api/call', methods=['POST'])
def api_call():
    d = request.json
    method_name = d.get('method')
    args = d.get('args', [])
    
    # Ha a kért funkció létezik a JsonDataManager-ben, végrehajtja
    if hasattr(db, method_name):
        func = getattr(db, method_name)
        try:
            result = func(*args)
            return jsonify({"status": "success", "result": result})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
            
    return jsonify({"status": "error", "message": "Funkció nem található"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)