import os
import json
import shutil
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='.', static_url_path='')

DATA_FILE = os.path.join('data', 'fish.json')
IMG_ROOT = 'img'

@app.route('/api/fish', methods=['GET'])
def get_fish():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fish', methods=['POST'])
def save_fish():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'no json'}), 400
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    cat = request.form.get('category', '').strip()
    sub = request.form.get('subcategory', '').strip()
    if not cat:
        return jsonify({'error': 'category required'}), 400
    target = os.path.join(IMG_ROOT, secure_filename(cat))
    if sub:
        target = os.path.join(target, secure_filename(sub))
    os.makedirs(target, exist_ok=True)
    paths = []
    for f in request.files.getlist('images'):
        filename = secure_filename(f.filename)
        if not filename:
            continue
        dest = os.path.join(target, filename)
        f.save(dest)
        rel = os.path.relpath(dest).replace('\\', '/')
        paths.append(rel)
    return jsonify({'paths': paths})

@app.route('/api/delete_file', methods=['POST'])
def delete_file():
    data = request.get_json()
    path = data.get('path') if data else None
    if not path:
        return jsonify({'error': 'path required'}), 400
    try:
        full = os.path.join(os.getcwd(), path)
        if os.path.exists(full) and os.path.isfile(full):
            os.remove(full)
            return jsonify({'status': 'deleted'})
        else:
            return jsonify({'error': 'not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete_folder', methods=['POST'])
def delete_folder():
    data = request.get_json()
    path = data.get('path') if data else None
    if not path:
        return jsonify({'error': 'path required'}), 400
    try:
        full = os.path.join(os.getcwd(), path)
        if os.path.isdir(full):
            shutil.rmtree(full)
            return jsonify({'status': 'deleted'})
        else:
            return jsonify({'error': 'not a directory'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# static route fallback
@app.route('/admin')
def admin_page():
    # explicit route so /admin works without .html
    return send_from_directory('.', 'admin.html')

@app.route('/<path:path>')
def static_proxy(path):
    # serve static files from project root
    return send_from_directory('.', path)

@app.route('/')
def root():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
