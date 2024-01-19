from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run_code', methods=['POST'])
def run_code():
    try:
        data = request.get_json()
        code = data['code']
        lang = data['language']
        custom_input = data.get('input', '')  # Custom input, optional

        if lang == 'python':
            cmd = ['python', '-c', code]
        else:
            return jsonify({'error': 'Unsupported language'}), 400

        result = subprocess.run(cmd, input=custom_input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output = result.stdout if result.returncode == 0 else result.stderr

        return jsonify({'output': output, 'error': result.returncode}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

