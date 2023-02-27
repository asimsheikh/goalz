from datetime import datetime 

from flask import Flask, request, render_template_string, render_template
from persist import Persist
from head import HEAD

db = Persist()
app = Flask(__name__)

def to_datetime(js_date: str) -> datetime:
    parsed_date = datetime.strptime(js_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return parsed_date

def to_js_date(date: datetime) -> str:
    return f"{date.isoformat()}Z"

@app.get('/routes')
def routes():
    route_urls = [str(rule) for rule in app.url_map.iter_rules()]
    page = '''
        <section class="ml-2">
            <ul>
            {% for route_url in data.route_urls %}
                <li>
                    <a href="{{route_url}}">{{ route_url }}</a>
                </li>
            {% endfor%}
            </ul>
        </section>
    '''
    return render_template_string(HEAD + page, data={'route_urls': route_urls})

@app.post('/api')
def api():
    action = request.form['action']
    if action == 'add_focus_area':
        return render_template_string(PAGE, data={'focus_areas': focus_areas})
    elif action == 'add_task':
        return 'Error' 
    else:
        return '<p class="bg-red-700 p-10">This is not a known action</p>'

@app.route('/')
def index():
    PAGE = '''This is a new page'''
    return render_template_string(HEAD + PAGE, data={})
