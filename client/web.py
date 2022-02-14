#!/usr/bin/env python3

import picoweb
import const
import machine
import ujson as json

ap_app = picoweb.WebApp(__name__)


@ap_app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite(wifi_setup_page)

@ap_app.route("/save")
def index(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        # Note: parse_qs() is not a coroutine, but a normal function.
        # But you can call it using yield from too.
        req.parse_qs()

    yield from picoweb.start_response(resp)
    print("XXXXXX", req.form)
    # write to wifi config
    f = open(const.WIFI_CONFIG_FILE, "w")
    f.write(json.dumps(req.form))
    f.close()
    yield from resp.awrite("Thanks! Chicory will try to connect to WIFI SSID: " + req.form["ssid"])
    # Reset machine
    machine.reset()

def run_ap(host):
    ap_app.run(debug=True, host = host)

def stop_ap():
    ap_app.stop()

wifi_setup_page = """
<html>
<head>
  <style>
    /* you can style your program here */
  </style>
</head>
<body>
  <main></main>
  <script>

  </script>
  <h1> Wifi Configuration </h1>
  <form action="/save">
      <label for="ssid">SSID:</label><br>
      <input type="text" id="ssidd" name="ssid"><br>
      <label for="password">Password:</label><br>
      <input type="text" id="password" name="password"><br><br>
      <input type="submit" value="Submit">
  </form>
</body>
</html>
"""
