import random
import json
import datetime
import datetime
import traceback
import sys

try:
    import dhttp

except ImportError:
    import __init__ as dhttp


app = dhttp.DHTTPServer(random.randint(8000, 8050) if sys.argv[1] == 'random' else (int(sys.argv[1]) if len(sys.argv) > 1 else 8000))

app.alias('/index', '/')
app.alias('/index.htm', '/')
app.alias('/index.html', '/')

test_index = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>My first DHTTP server</title>
</head>

<body>
    <p><h2>Congratulations!</h2></p>
    <hr>
    <p><b>dhttp {version}</b> is now running on your machine.</p>
    <p>How about <i>{party}</i> to comemorate? :)</p>
    <br/>
    <p><small>{time}</small></p>
</body>
</html>"""

party_stuff = [
    'a bottle of wine', 'a bottle of champagne', 'a big party',
    'THE party, just', 'THE party', 'lots of cats', 'partyception',
    'balloons and cakes', 'a big-endian cake', 'lots of confetti',
    'the Confetti-o-Tron 2000', 'HTTP juice', 'Spicy Bytes',
    'antimatter', 'cats writing code', 'a smile breaking the 4th wall'
]

@app.get('/')
def serve_index(req, res):
    res.end(test_index.format(
        party = res['party'],
        time = res['time'],
        version = dhttp.DHTTP_VERSION
    ))

@app.on_log
def print_log(log):
    if log.request.get_header('X-Forwarded-For') is not None:
        log.ip = log.request.get_header('X-Forwarded-For')
        print(log, '  (forwarded)')

    else:
        print(log)

@app.use()
def set_party(req, res):
    this_party = random.choice(party_stuff)
    res['party'] = this_party

    utc = datetime.datetime.utcnow()
    res['time'] = f"Right now, in the UTC, this {utc.strftime('%A')} it's {utc.strftime('%H:%M:%S')}."

    if req.resolve_path() == '/':
        print(dhttp.DHTTPGenericLog("PARTY", f"And now, {this_party} to comemorate!"))

app.static('/static',  './static')
app.static('/src/jinja', './static/jinja')

log = []
clients = set()
nick = {}
bad = set()

@app.jinja_folder('/jinja', './static/jinja')
async def jinja_folder(req, set, done):
    set('utctime', datetime.datetime.utcnow().strftime('%H:%M:%S'))
    set('upper_log', log)
    done()

@app.websocket('/ws/upper')
def uppercase_stuff(client, res):
    clients.add(client) 

    @client.ws_receiver
    def make_me_uppercase(data):
        try:
            msg = json.loads(data.content.decode('utf-8'))

        except json.JSONDecodeError:
            return

        if 'content' not in msg or 'type' not in msg:
            return

        msg['content'] = msg['content'][:400]

        if msg['type'] == 'message' and id(client) in nick and id(client) not in bad:
            log.append((nick[id(client)], msg['content']))

            for c in clients:
                c.ws_write(f"MSG {nick[id(client)]} {msg['content']}")

        elif msg['type'] == 'nick':
            msg['content'] = msg['content'].encode('utf-8').decode('ascii', errors='ignore')[:40]

            if msg['content'] not in nick.values():
                if id(client) in bad:
                    bad.remove(id(client))

                nick[id(client)] = msg['content']
                client.ws_write(f"NICK yes")

            else:
                bad.add(id(client))
                client.ws_write(f"NICK no")

    @client.on_close
    def make_me_dead(_):
        clients.remove(client)

@app.on_response_finish
def on_served(req, res):
    print(dhttp.DHTTPGenericLog("INFO", f"Served {req.method} to '{req.path}'"))    

@app.on_response_error
def catch_error(call, err):
    print(dhttp.DHTTPGenericLog("ERR!", f'Caught {type(err).__name__} trying to run {call[3]}! Ignoring...'))
    print(f' -> {str(err)}')
    traceback.print_tb(err.__traceback__)

@app.run_forever
def on_serve():
    print(f"   == Listening on port: {app.port} ==")