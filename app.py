from flask import Flask, request, render_template_string
from persist import Persist
from head import HEAD
from models import FocusArea 

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
                    # hx-vals='{ "action": "add_focus_area" }'
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
        '''
        focus_areas = [ FocusAreaView(FocusArea(**focus_area)) for focus_area in db.get('focus_areas') ]
        return render_template_string(PAGE, data={'focus_areas': focus_areas})
    return ''

@app.route('/')
def index():
    PAGE = '''
            <div class="m-2" id="add_focus_area">
                <form class="m-2 flex flex-col" 
                    hx-post="/api"
                    hx-target="[id='add_focus_area']"
                    # hx-vals='{ "action": "add_focus_area" }'
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
    '''

    focus_areas = [ FocusAreaView(FocusArea(**focus_area)) for focus_area in db.get('focus_areas') ]
    return render_template_string(HEAD + PAGE, data={'focus_areas': focus_areas})
