from sklearn.externals import joblib
from flask import Flask
from flask import json
from flask import request

logistic = joblib.load('trained_logistic.pkl')

app = Flask(__name__)

@app.route('/check', methods = ['POST'])
def check():
    content = request.json
    x_test = [content['cpu-usage'], content['context-switch'], content['cpu-migration'], content['page-faults'],
              content['cycles-GHz'], content['stalled-cycles-frontend-percent'],
              content['stalled-cycles-backend-percent'], content['Instructions-per-cycle'],
              content['stalled-cycles-per-instruction'], content['branches'], content['branch-misses-percent'],
              content['bus-cycle'], content['cache-misses-percent'], content['cache-references'], content['ref-cycles']]
    y_predict_logistic_con = logistic.predict_proba([x_test])
    return  json.dumps({"name" :content['name'],"possibility" : str("{0:.3f}".format(y_predict_logistic_con[0][1]))})


@app.route('/group_check', methods = ['POST'])
def group_check():
    objects = request.json
    result = {}
    for index , content in enumerate(objects):
        x_test = [content['cpu-usage'], content['context-switch'], content['cpu-migration'], content['page-faults'],
                  content['cycles-GHz'], content['stalled-cycles-frontend-percent'],
                  content['stalled-cycles-backend-percent'], content['Instructions-per-cycle'],
                  content['stalled-cycles-per-instruction'], content['branches'], content['branch-misses-percent'],
                  content['bus-cycle'], content['cache-misses-percent'], content['cache-references'],
                  content['ref-cycles']]
        y_predict_logistic_con = logistic.predict_proba([x_test])
        result[content['name']] = str("{0:.3f}".format(y_predict_logistic_con[0][1]))
    return  json.dumps(result)


if __name__ == "__main__":
    app.run(host= '0.0.0.0')