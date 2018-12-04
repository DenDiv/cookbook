from suggester import *
from flask import Flask, json, jsonify
from classif import *
from invert_ind import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/get_ingr/<prefix>', methods=['GET'])
def get_ingr(prefix):
    prefix = prefix.lower().replace('ё', 'е')
    my_str = ', '.join(list(data[data.name==prefix].ingredients)[0])
    return my_str

@app.route('/get_suggest/<prefix>', methods=['GET'])
def suggestions(prefix):
    suggest = suggester(root, prefix)
    sug_string = ''
    for i in suggest:
        sug_string += i + '<br>'
    return sug_string

@app.route('/get_best_suggest/<prefix>', methods=['GET'])
def rat(prefix):
    suggest = rating(root, prefix, 10, data)
    sug_string = ''
    for i in suggest:
        sug_string += i + '<br>'
    return sug_string

@app.route('/classif/<prefix>', methods=['GET'])
def pred_class(prefix):
    return pred(prefix,clf,ingr_l)

@app.route('/find_rec/<prefix>', methods=['GET'])
def get_rec(prefix):
    str_rec = ''
    set_rec = get_recipes_many(prefix,df)
    for i in set_rec:
        str_rec += i + '<br>'
    return str_rec

if __name__ == "__main__":

    #suggester
    data = pd.read_json('cook_dataset.json')
    data['name'] = data['name'].apply(lambda x: x.lower().replace('ё', 'е'))
    root = TrieNode('*')
    for i in data['name']:
        add(root, i)
    #classif
    (clf,ingr_l) = classif()
    #invert_ind
    with open('df_classif.pickle', 'rb') as f:
        df = pickle.load(f)
    app.run()
