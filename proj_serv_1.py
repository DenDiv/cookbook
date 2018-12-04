from suggester import *
from flask import Flask, json, jsonify, render_template, request, flash, redirect, url_for, get_flashed_messages
from classif import *
from invert_ind import *
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.urandom(24)

@app.route('/get_ingr/<prefix>', methods=['GET'])
def get_ingr(prefix):
    name = get_flashed_messages()[0]
    prefix = prefix.lower().replace('ё', 'е')
    my_str = list(data[data.name == prefix].ingredients)[0]
    return render_template('get_ingr_page.html', name=name, ingredients=my_str)

@app.route('/ingredients', methods=['POST', 'GET'])
def help_ingr():
    if request.method == 'POST':
        name = request.form["Name"]
        flash(name)
        return redirect(url_for('get_ingr', prefix=name))


@app.route('/get_suggest/<prefix>', methods=['GET'])
def suggestions(prefix):
    suggest = suggester(root, prefix)
    #sug_string = ''
    #for i in suggest:
    #    sug_string += i + '<br>'
    return render_template('get_suggest_page.html', name=prefix, suggestions=suggest)

@app.route('/suggestions', methods=['POST', 'GET'])
def help_suggest():
    if request.method == 'POST':
        name = request.form["Name"]
        flash(name)
        return redirect(url_for('suggestions', prefix=name))


@app.route('/get_best_suggest/<prefix>', methods=['GET'])
def rat(prefix):
    suggest = rating(root, prefix, 10, data)
    #sug_string = ''
    #for i in suggest:
    #    sug_string += i + '<br>'
    return render_template('get_rat_page.html', name=prefix, top10=suggest)

@app.route('/top10', methods=['POST', 'GET'])
def help_rat():
    if request.method == 'POST':
        name = request.form["Name"]
        flash(name)
        return redirect(url_for('rat', prefix=name))

@app.route('/classif/<prefix>', methods=['GET'])
def pred_class(prefix):
    return render_template('get_pred_class_page.html', name=prefix, cls=pred(prefix, clf, ingr_l))

@app.route('/classif', methods=['POST', 'GET'])
def help_pred_class():
    if request.method == 'POST':
        name = request.form["Name"]
        flash(name)
        return redirect(url_for('pred_class', prefix=name))


@app.route('/find_rec/<prefix>', methods=['GET'])
def get_rec(prefix):
    #str_rec = ''
    set_rec = get_recipes_many(prefix, df)
    #for i in set_rec:
    #    str_rec += i + '<br>'
    return render_template('get_rec_page.html', name=prefix, rec=set_rec)

@app.route('/rec', methods=['POST', 'GET'])
def help_rec():
    if request.method == 'POST':
        name = request.form["Name"]
        flash(name)
        return redirect(url_for('get_rec', prefix=name))

@app.route('/')
def start():
    return render_template('start_page.html')


if __name__ == "__main__":
    #suggester
    data = pd.read_json('cook_dataset.json')
    data['name'] = data['name'].apply(lambda x: x.lower().replace('ё', 'е'))
    root = TrieNode('*')
    for i in data['name']:
        add(root, i)
    #classif
    (clf, ingr_l) = classif()
    #invert_ind
    with open('df_classif.pickle', 'rb') as f:
        df = pickle.load(f)
    app.run(debug=True)
