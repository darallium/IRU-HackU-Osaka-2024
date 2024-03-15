from flask import Flask, render_template, request
import json
import shutil

app = Flask(__name__)

def load_config():
    with open('config.json', 'r') as f:
        data = json.load(f)
    return data

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'reset' in request.form:
            shutil.copyfile('default_config.json', 'config.json')
        else:
            new_data = request.form.to_dict()
            with open('config.json', 'w') as f:
                json.dump(new_data, f, indent=4)
    data = load_config()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
