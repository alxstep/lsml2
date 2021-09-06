import os
from celery.result import AsyncResult
from flask import render_template, Blueprint, jsonify, request, flash, Flask, redirect, url_for, current_app
from werkzeug.utils import secure_filename

from tasks import create_task


main_blueprint = Blueprint("main", __name__,)


@main_blueprint.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if not file.filename.rsplit('.', 1)[1].lower() in ('jpg', 'jpeg'):
            flash('File format is not allowed')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))            
            flash('File was successfully uploaded')
            return redirect(request.url)

    params = { 
            "images": os.listdir(current_app.config['UPLOAD_FOLDER']) 
        }

    return render_template("index.html", params=params)


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    img_name = content["name"]
    task = create_task.delay(img_name)
    return jsonify({"task_id": task.id}), 201


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200
