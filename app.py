import math
from tempfile import tempdir
from flask import Flask, redirect , render_template ,request
import pickle

app = Flask(__name__)
model = pickle.load(open('xgboost_model_v3.pkl','rb'))
scaler = pickle.load(open('scaler.pkl','rb'))


@app.route('/')
def home_page():
    return render_template('index.html')


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

@app.route('/result' ,methods=['POST'])
def predict():
    if request.method == 'POST':
        temp = float(request.form['temp'])
        humidity = float(request.form['humidity'])
        wind = float(request.form['wind'])
        general_diff = float(request.form['general_diff'])
        diff = float(request.form['diff'])


        var = [[temp,humidity,wind,general_diff,diff]]
        #var = scaler.transform(var)
        result = model.predict(var)
        r0= ("%s - %s" % ((round_up(result[0][0],-3)-500),(round_up(result[0][0],-3)+500)))
        r1=("%s - %s" % ((round_up(result[0][1],-3)-500),(round_up(result[0][1],-3)+500)))
        r2=("%s - %s" % ((round_up(result[0][2],-3)-500),(round_up(result[0][2],-3)+500)))
        style = '<stlye> \
                .result{display:block;}</style>'
        
        return render_template('result.html',temp=temp,hum=humidity,wind=wind,general_diff=general_diff,diff=diff,z0=r0,z1=r1,z2=r2)

if __name__ == '__main__':
    app.run(debug=True)