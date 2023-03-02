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
    payload = eval(request.form['payload'])
    if action == 'toggle_pebble':
        # get the pebble with id and reverse
        # update the db with new pebble status
        # return the colored pebble        
        pd = [ pebble for pebble in db.get('pebbles') if pebble['id'] == payload['id'] ][0]
        status = not pd['status']
        db.update('pebbles', payload['id'], {'id': payload['id'], 'status': status})
        pebble = f'''<div class="pebble {'active' if status else 'inactive'}"
                data-tooltip="{payload['id']}"
                hx-post="/api"
                hx-vals='{{ "action": "toggle_pebble", "payload": {{"id": "{payload['id']}"}} }}'
                hx-swap="outerHTML">
            <p></p>
        </div>'''
        return pebble
    elif action == 'add_task':
        return 'Error' 
    else:
        return '<p class="bg-red-700 p-10">This is not a known action</p>'

@app.route('/grid')
def grid():
    return render_template('grid.html')

@app.route('/')
def index():
    PAGE = ''' 
            <style>
            #pebbles {
                margin: 2rem;
                display: grid;
                grid-template-rows: repeat(4, auto);
                grid-template-columns: repeat(24, auto);
            }

             .pebble {
                margin: 0.5rem;
                width: 2rem;
                height: 2rem;
                position: relative;
            }

            .pebble:hover::after {
                position: absolute;
                top: -1.5rem;
                left: 1rem;
                content: attr(data-tooltip);
                background: #000000bd;
                color: white;
                padding: 0.5rem;
            }

             .active {
                background-color: green;
             }

            .inactive {
                background-color: #f443361a;
            }

            #grid {
                display: grid;
            }

            </style>
            <script>
                onClick = (e) => {
                    console.log(e)
                    e.preventDefault()
                    let menu = document.createElement("div")
                    menu.id = "ctxmenu"
                    menu.style = `top:${e.pageY-10}px;left:${e.pageX-40}px`
                    menu.onmouseleave = () => ctxmenu.outerHTML = ''
                    menu.innerHTML = "<p>Option1</p><p>Option2</p><p>Option3</p><p>Option4</p><p onclick='alert(`Thank you!`)'>Upvote</p>"
                    document.getElementById("pebbles").appendChild(menu)
                }
            </script>
            <body>
                <section id="pebbles" ondblclick="onClick(event)">
                {% for pebble in data.pebbles %}
                    <div class="pebble {{ 'active' if pebble.status else 'inactive'}}"
                        data-tooltip="{{ pebble.id }}"
                        hx-post="/api"
                        hx-vals='{ "action": "toggle_pebble", "payload": {"id": "{{ pebble.id }}" }}'
                        hx-swap="outerHTML">
                        <p></p>
                    </div>
                {% endfor%}
                </section>
            </body>
    '''
    return render_template_string(HEAD + PAGE, data={'pebbles': db.get('pebbles')})
