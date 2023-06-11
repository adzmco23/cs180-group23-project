from flask import Flask, request, render_template

from app.regression import Model

app = Flask(__name__)

m: Model = Model()

# render webpage
@app.get("/")
def home():
    return render_template('index.html')

# route for calculating food price using regression model
@app.get("/price")
def foodPrice():

    ### SAMPLE GET request: http://localhost:5000/price?year=2023&month=5&commodity=eggs&pricetype=wholesale

    req = request.args.to_dict()
    year = int(req['year'])
    month = int(req['month'])
    commodity = req['commodity']
    pricetype = req['pricetype']

    print(req)
    param = {'year':year, 'month': month, 'latitude':14.604167, 'longitude':120.982222, 'inflation':6.6}
    param.update({commodity: 1})
    param.update({pricetype:1})
    print(param)
    return str(m.getPrice(param))

if __name__ == "__main__":
    app.run(debug=True)