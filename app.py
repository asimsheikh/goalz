from flask import Flask, request, render_template_string
from persist import Persist
from head import HEAD
from models import FocusArea, Task

db = Persist()
app = Flask(__name__)

class FocusAreaView:
    def __init__(self, focus_area: FocusArea):
        self.focus_area = focus_area

    def render(self):
        return f'''
                <div id="{self.focus_area.id}" class="flex">
                <div>
                    <p>{self.focus_area.name}</p>
                </div>
                <button class="ml-2 border-zinc-700 border-2 px-2 rounded-md hover:bg-neutral-900 hover:text-neutral-200"
                    hx-post="/api"
                    hx-trigger="click"
                    hx-target="[id='{self.focus_area.id}']"
                    hx-vals='{{"id": "{self.focus_area.id}", "action": "edit_focus_area" }}'
                    hx-swap="outerHTML">Edit</button>
                <button class="ml-2 border-zinc-700 border-2 px-2 rounded-md hover:bg-neutral-900 hover:text-neutral-200"
                    hx-post="/api"
                    hx-trigger="click"
                    hx-target="[id='{self.focus_area.id}']"
                    hx-vals='{{"id": "{self.focus_area.id}", "action": "delete_focus_area" }}'
                    hx-swap="outerHTML">Delete</button>
                </div>
        '''

    def edit(self):
        return f'''
                <div id="{self.focus_area.id}">
                    <div class="m-4">
                        <p class="text-lg">Focus Area</p>
                        <p class="text-sm">The areas in life you are focused on</p>
                    </div>
                    <form class="m-2 flex flex-col" 
                        hx-post="/api"
                        hx-target="[id='{self.focus_area.id}']"
                        hx-vals='{{"id": "{self.focus_area.id}", "action": "update_focus_area" }}'
                        hx-swap="outerHTML">
                        <div class="flex flex-row">
                            <div class="flex flex-col border-2 rounded-md w-4/12 mx-2 p-2">
                                <label class="text-sm" for="focus_area_name">Update Focus Area</label>
                                <input type="text" value="{self.focus_area.name}" name="focus_area_name" id="focus_area_name" autofocus onfocus="this.select()"/>
                            </div>
                        </div>
                            <div>
                                <input class="bg-black text-white px-4 m-2 py-2 w-1/12 rounded-md" type="submit" value="Save" />
                            </div>
                    </form>
                </div>
                '''

@app.post('/testing')
def testing():
    json = request.json or {}
    if json and json['action'] == 'add_comment':
        # return json['payload']
        return '<p>Comment</p>'

    if 'name' in request.form:
        return '<p class="text-xl">help to gym</p>'

    return 'Nothing'

@app.get('/comments')
def comments():
    return 'Comments section'

@app.get('/routes')
def routes():
    route_urls = [str(rule) for rule in app.url_map.iter_rules()]
    page = '''
        <section>
            <ul>
            {% for route_url in data.route_urls %}
                <li>
                    <a href="{{route_url}}">{{ route_url }}</a>
                </li>
            {% endfor%}
            </ul>
        </section>
    '''
    return render_template_string(page, data={'route_urls': route_urls})

@app.post('/api')
def api():
    action = request.form['action']
    if action == 'add_focus_area':
        db.add('focus_areas', FocusArea(name=request.form['focus_area_name']).dict())  # type: ignore
        PAGE = '''
            <div class="m-2" id="add_focus_area">
                <form class="m-2 flex flex-col" 
                    hx-post="/api"
                    hx-target="[id='add_focus_area']"
                    hx-vals='{ "action": "add_focus_area" }'
                    hx-swap="outerHTML">
                    <div class="flex flex-row">
                        <div class="flex flex-col rounded-md w-4/12 mx-2 p-2">
                            <label class="text-xl font-semibold" for="focus_area_name">Add Focus Area</label>
                            <input class="p-2 border-2 rounded-md" type="text" value="" name="focus_area_name" id="focus_area_name" autofocus onfocus="this.select()"/>
                            <input class="bg-black text-white my-2 py-2 rounded-md w-1/3" type="submit" value="Add" />
                        </div>
                    </div>
                </form>
            </div>
            <div class="m-2" id="focus_areas" hx-swap-oob="true">
                <p class="text-2xl py-2 font-semibold">Focus Areas</p>
                 {% for focus_area in data.focus_areas %}
                    {{ focus_area.render() | safe }}
                 {% endfor%}
            </div>
            <div>
              <p>Focus area tasks</p>
            </div>
        '''
        focus_areas = [ FocusAreaView(FocusArea(**focus_area)) for focus_area in db.get('focus_areas') ]
        return render_template_string(PAGE, data={'focus_areas': focus_areas})
    elif action == 'delete_focus_area':
        db.delete('focus_areas', request.form['id'])
        return ''
    elif action == 'add_task':
        print(request.form)
        task = Task(name=request.form['task_name'], focus_area_id=request.form['focus_area_id'])
        db.add('tasks', task.dict())
        focus_areas = [ FocusAreaView(FocusArea(**focus_area)) for focus_area in db.get('focus_areas') ]
        PAGE = '''
            <div id="add_task">
              <p class="bg-red-100 p-2">Focus area tasks</p>
                <form class="m-2 flex flex-col" 
                    hx-post="/api"
                    hx-target="[id='add_task']"
                    hx-vals='{ "action": "add_task" }'
                    hx-swap="outerHTML">
                    <div class="flex flex-row">
                        <div class="flex flex-col rounded-md w-4/12 mx-2 p-2">
                            <label class="text-xl font-semibold" for="add_task">Add Task</label>
                            <input class="p-2 border-2 rounded-md" type="text" value="" name="task_name" id="task_name" autofocus onfocus="this.select()"/>
                            <select class="p-2 border-2 rounded-md w-1/2" name="focus_area_id" id="focus_area_id">
                            {% for focus_area in data.focus_areas %}
                                <option value="{{focus_area.focus_area.id}}">{{ focus_area.focus_area.name}}</option>
                            {% endfor %}
                            </select>
                            <input class="bg-black text-white my-2 py-2 rounded-md w-1/3" type="submit" value="Add" />
                        </div>
                    </div>
                </form>
            </div>
            <div class="m-2" id="tasks" hx-swap-oob="true">
                <p class="text-2xl py-2 font-semibold">Tasks</p>
                <div class="">
                 {% for task in data.tasks %}
                    <p>{{ task.name }} | {{ task.focus_area_id }}</p>
                 {% endfor%}
                </div>
            </div>
        '''
        focus_areas = [ FocusAreaView(FocusArea(**focus_area)) for focus_area in db.get('focus_areas') ]
        return render_template_string(HEAD + PAGE, data={'focus_areas': focus_areas, 'tasks': db.get('tasks')})
    else:
        return '<p class="bg-red-700 p-10">This is not a known action</p>'

@app.route('/')
def index():
    PAGE = '''
            <div class="m-2" id="add_focus_area">
                <form class="m-2 flex flex-col" 
                    hx-post="/api"
                    hx-target="[id='add_focus_area']"
                    hx-vals='{ "action": "add_focus_area" }'
                    hx-swap="outerHTML">
                    <div class="flex flex-row">
                        <div class="flex flex-col rounded-md w-4/12 mx-2 p-2">
                            <label class="text-xl font-semibold" for="focus_area_name">Add Focus Area</label>
                            <input class="p-2 border-2 rounded-md" type="text" value="" name="focus_area_name" id="focus_area_name" autofocus onfocus="this.select()"/>
                            <input class="bg-black text-white my-2 py-2 rounded-md w-1/3" type="submit" value="Add" />
                        </div>
                    </div>
                </form>
            </div>
            <div class="m-2" id="focus_areas">
                <p class="text-2xl py-2 font-semibold">Focus Areas</p>
                <div class="">
                 {% for focus_area in data.focus_areas %}
                    {{ focus_area.render() | safe }}
                 {% endfor%}
                </div>
            </div>
            <div class="m-2" id="tasks" hx-swap-oob="true">
                <p class="text-2xl py-2 font-semibold">Tasks</p>
                <div class="">
                 {% for task in data.tasks %}
                    <p>{{ task.name }}</p>
                 {% endfor%}
                </div>
            </div>
            <div id="add_task">
              <p class="bg-red-100 p-2">Focus area tasks</p>
                <form class="m-2 flex flex-col" 
                    hx-post="/api"
                    hx-target="[id='add_task']"
                    hx-vals='{ "action": "add_task" }'
                    hx-swap="outerHTML">
                    <div class="flex flex-row">
                        <div class="flex flex-col rounded-md w-4/12 mx-2 p-2">
                            <label class="text-xl font-semibold" for="add_task">Add Task</label>
                            <input class="p-2 border-2 rounded-md" type="text" value="" name="task_name" id="task_name" autofocus onfocus="this.select()"/>
                            <select class="p-2 border-2 rounded-md w-1/2" name="focus_area_id" id="focus_area_id">
                            {% for focus_area in data.focus_areas %}
                                <option value="{{focus_area.focus_area.id}}">{{ focus_area.focus_area.name}}</option>
                            {% endfor %}
                            </select>
                            <input class="bg-black text-white my-2 py-2 rounded-md w-1/3" type="submit" value="Add" />
                        </div>
                    </div>
                </form>
            </div>
    '''

    focus_areas = [ FocusAreaView(FocusArea(**focus_area)) for focus_area in db.get('focus_areas') ]
    return render_template_string(HEAD + PAGE, data={'focus_areas': focus_areas, 'tasks': db.get('tasks')})

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return str(list(request.form.items()))
    PAGE = '''
    <body>
        <div class="ml-4">
            <p class="text-xl font-bold">Hello World</p>
            <p>Then entering some more text</p>
            <ul class="ml-6 list-disc">
              <li>Test the idea of using formData object on forms</li>
            </ul>
        </div>
        <div class="ml-4 mt-4">
            <form hx-post="/test" hx-target="#form-data">
                <p>
                    <label for="first-name">First Name</label>
                    <input id="first-name" name="first-name" type="text" class="border-2" value="Asim Sardar"/>
                </p>
                <p>
                    <label for="last-name">Last Name</label>
                    <input id="last-name" name="last-name" type="text" class="border-2" value="Sheikh"/>
                </p>
                <p>
                    <input type="submit" class="border-2 p-2" value="Send"/>
                </p>
            </form>
        </div>
        <div id="form-data" class="ml-4 mt-4">
        </div>
    </bodv>
    '''
    return render_template_string(HEAD + PAGE)