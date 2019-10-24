from flask import Flask, request, url_for, abort, redirect
from application import url_shortener, url_resolver

app = Flask(__name__)

# TODO(noam): A real application would have some sort of config for the base URL
# it's bound to

@app.route('/go/<shortname>')
def resolve_shortname(shortname):
    url = url_resolver.resolve_url(shortname)

    if url == None:
        abort(404)

    return redirect(url.url)

@app.route('/create', methods=['POST'])
def create_shortname():
    url = url_shortener.shorten_url(request.form['url'])

    return {
        'url': "%sgo/%s" % (request.url_root, url.shortname)
    }
