import os
import sys
import io
from flask import Flask, request, jsonify,send_file
import traceback
import subprocess
app = Flask(__name__)



@app.route('/code/execute', methods=['POST'])
def execute_code():
    try:
        # Obtenir le code depuis le corps de la requête
        data = request.get_json()
        code = data.get("command", "")

        if not code:
            return jsonify({"error": "Aucun code fourni."}), 400

        # Dictionnaire pour l'espace de variables globales
        variables = {}

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            # Exécuter le code
            exec(code, variables)
            # Récupérer la sortie standard capturée
            result = sys.stdout.getvalue()
        finally:
            # Restaurer sys.stdout
            sys.stdout = old_stdout


        return jsonify({
            'status': 'success',
            'result': result
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 500
    
@app.route('/manim/create', methods=['POST'])
def execute_command():
    try:
        #identifier = request.args.get('identifier', '')
        data = request.json
        manim= data.get('manim',"")
        pyfile= manim.get('pyfile',"")
        videofile= manim.get('videofile',"")
        command = manim.get('command',"")
        pythoncode= manim.get('pythoncode',"")
        if not pyfile:
            return jsonify({'status': 'error', 'message': 'No python file provided'}), 400
        if not videofile:
            return jsonify({'status': 'error', 'message': 'No video file provided'}), 400
        if not command:
            return jsonify({'status': 'error', 'message': 'No command provided'}), 400
        if not pythoncode:
            return jsonify({'status': 'error', 'message': 'No python code provided'}), 400
        
        with open(pyfile, 'w') as file: file.write(pythoncode)
        # Exécuter la commande avec un timeout de 60 secondes
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=600)

        if result.returncode == 0:
            return jsonify({'status': 'success', 'output': result.stdout}), 200
        else:
            return jsonify({'status': 'error', 'message': result.stderr}), 400

    except subprocess.TimeoutExpired:
        return jsonify({'status': 'error', 'message': 'Command timed out'}), 408

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/manim/get_video', methods=['POST'])
def get_video():
    data = request.json
    videofile = data.get('videofile',"") 

    if not videofile:
        return jsonify({'status': 'error', 'message': 'No video file specified'}), 400

    if not os.path.exists(videofile):
        return jsonify({'status': 'error', 'message': 'Video file not found'}), 404

    return send_file(videofile, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
