from flask import Blueprint, jsonify, request

from app.services import FishService, api_handler


api_bp = Blueprint("api", __name__)
_service = FishService()


@api_bp.get("/fish")
@api_handler
def get_fish():
    data = _service.list_fish()
    return jsonify(data)


@api_bp.post("/fish")
@api_handler
def save_fish():
    payload = request.get_json(silent=True)
    _service.save_fish(payload)
    return jsonify({"status": "ok"})


@api_bp.post("/upload")
@api_handler
def upload():
    category = request.form.get("category", "")
    subcategory = request.form.get("subcategory", "")
    paths = _service.upload_images(
        category=category,
        subcategory=subcategory,
        files=request.files.getlist("images"),
    )
    return jsonify({"paths": paths})


@api_bp.post("/delete_file")
@api_handler
def delete_file():
    data = request.get_json(silent=True) or {}
    result = _service.delete_file(data.get("path"))
    return jsonify(result)


@api_bp.post("/delete_folder")
@api_handler
def delete_folder():
    data = request.get_json(silent=True) or {}
    result = _service.delete_folder(data.get("path"))
    return jsonify(result)

