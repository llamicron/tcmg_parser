import json

from flask import Flask, render_template, request

from parse import parse


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

app = CustomFlask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=["POST"])
def serve_parsed_data():
    url = request.data.decode('utf-8')
    return json.dumps(parse(url))

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=5000)
