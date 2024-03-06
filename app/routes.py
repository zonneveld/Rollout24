from app import app
from app.hardware import TaskMaster

from flask import request, render_template

taskmaster = TaskMaster()
taskmaster.start()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/action', methods=['POST'])
def action():
    action_data = request.json
    for action in action_data['actions']:
        taskmaster.add_task(action)

    return {},200