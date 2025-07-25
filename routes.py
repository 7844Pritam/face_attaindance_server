from flask import Blueprint, request, jsonify
from datetime import datetime
from face_utils import load_known_faces, recognize_face, save_new_employee

face_routes = Blueprint('face_routes', __name__)
known_faces, known_names = load_known_faces()

@face_routes.route('/', methods=['GET'])
def ping():
    return jsonify({'status': 'ok', 'message': 'Face recognition server is running'}), 200


@face_routes.route('/verify', methods=['POST'])
def verify():
    global known_faces, known_names

    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image uploaded'}), 400

    file = request.files['image']
    result = recognize_face(file, known_faces, known_names)

    if result:
        name, confidence = result
        return jsonify({
            'success': True,
            'name': name,
            'confidence': confidence,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    else:
        return jsonify({'success': False, 'message': 'Face not recognized'}), 401

@face_routes.route('/add_employee', methods=['POST'])
def add_employee():
    global known_faces, known_names

    name = request.form.get('name')
    image = request.files.get('image')

    if not name or not image:
        return jsonify({'success': False, 'message': 'Missing name or image'}), 400

    success = save_new_employee(name, image)

    if success:
        known_faces, known_names = load_known_faces()
        return jsonify({'success': True, 'message': 'Employee added'})
    else:
        return jsonify({'success': False, 'message': 'Failed to add employee'}), 500
