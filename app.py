from flask import Flask, request, render_template_string
from persist import Persist
from head import HEAD
from models import Task

db = Persist()
app = Flask(__name__)


@app.post('/api')
def api():
    if  request.form.get('action') == 'edit_task':
        task_id = request.form['id']
        task = [task for task in db if task.id == task_id][0]
        return render_template_string(task.edit())
    elif request.form.get('action') == 'update_task':
        task_id = request.form['id']
        task_name = request.form['task_name']
        for task in db:
            if task.id == task_id:
               task.name = task_name
               return render_template_string(task.render())
        raise TypeError
    elif request.form.get('action') == 'add_task':
        task_name: str = request.form.get('task_name') or ''
        db.append(Task(name=task_name))
        form = ''' 
            <div class="m-2" id="add_task">
                <form class="m-2 flex flex-col" 
                    hx-post="/api"
                    hx-target="[id='add_task']"
                    hx-swap="outerHTML">
                    <div class="flex flex-row">
                        <div class="flex flex-col rounded-md w-4/12 mx-2 p-2">
                            <label class="text-xl font-semibold" for="task_name">Add Task</label>
                            <input class="p-2 border-2 rounded-md" type="text" value="" name="task_name" id="task_name" autofocus onfocus="this.select()"/>
                            <input type="hidden" id="action" name="action" value="add_task">
                            <input class="bg-black text-white my-2 py-2 rounded-md w-1/3" type="submit" value="Add" />
                        </div>
                    </div>
                </form>
            </div>
            <div class="m-2" id="tasks" hx-swap-oob="true">
                <p class="text-2xl py-2 font-semibold">Tasks</p>
                {%for task in data.tasks %}
                    {{ task.render() | safe }}
                {% endfor%}
            </div>
        '''
        return render_template_string(form, data={'tasks': db})
    elif request.form.get('action') == 'delete_task':
        task_id = request.form['id']        
        db = [ task for task in db if task.id != task_id]
        return ''
    else:
        raise TypeError

@app.route('/')
def index():
    DATA_PAGE = '''
        <div class="w-1/2">
            <pre class="w-1/2">{{data}}</pre>
        </div>
    '''
    PAGE = '''
            <div class="m-2" id="add_task">
                <form class="m-2 flex flex-col" 
                    hx-post="/api"
                    hx-target="[id='add_task']"
                    hx-swap="outerHTML">
                    <div class="flex flex-row">
                        <div class="flex flex-col rounded-md w-4/12 mx-2 p-2">
                            <label class="text-xl font-semibold" for="task_name">Add Task</label>
                            <input class="p-2 border-2 rounded-md" type="text" value="" name="task_name" id="task_name" autofocus onfocus="this.select()"/>
                            <input type="hidden" id="action" name="action" value="add_task">
                            <input class="bg-black text-white my-2 py-2 rounded-md w-1/3" type="submit" value="Add" />
                        </div>
                    </div>
                </form>
            </div>
            <div class="m-2" id="tasks">
                <p class="text-2xl py-2 font-semibold">Tasks</p>
                {%for task in data.tasks %}
                {{ task.render() | safe }}
                {% endfor%}
            </div>
    '''
    return render_template_string(HEAD + '<body>' + PAGE + '</body>', data={'tasks': db})
