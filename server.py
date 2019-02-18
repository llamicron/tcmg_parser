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
app.log_url = 'https://s3.amazonaws.com/tcmg476/http_access_log'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select-log', methods=['POST'])
def select_log():
    app.log_url = request.data.decode('utf-8')
    return 'True'

@app.route('/data', methods=["GET"])
def serve_data():
    return json.dumps(parse(app.log_url))

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=5000)
