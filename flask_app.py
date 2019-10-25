from flask import Flask, request, url_for, abort, redirect
from application import url_shortener, url_resolver, stat_processor, stat_reader
from stats.stat_thread import StatThread
from stats.stat_processor import StatDatapoint
from datetime import datetime

app = Flask(__name__)

stat_thread = StatThread(stat_processor)
stat_thread.start()

@app.route('/go/<shortname>')
def resolve_shortname(shortname):
    url = url_resolver.resolve_url(shortname)

    if url == None:
        abort(404)

    stat_thread.push_datapoint(StatDatapoint(url_id = url.id,
        time_accessed = datetime.now()))
    return redirect(url.url)

@app.route('/create', methods=['POST'])
def create_shortname():
    url = url_shortener.shorten_url(request.form['url'])

    return {
        'url': "%sgo/%s" % (request.url_root, url.shortname)
    }

@app.route('/stat/<shortname>')
def get_stats(shortname):
    stats = stat_reader.get_stats(shortname)

    if stats == None:
        abort(404)

    return {
        'all_time': stats.all_time
    }
