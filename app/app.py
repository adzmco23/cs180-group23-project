from flask import Flask, request, render_template

from app.regression import Model

app = Flask(__name__)

m: Model = Model()

# render webpage
@app.get("/")
def hello():
    return render_template('index.html')

# route for calculating food price using regression model
@app.get("/price")
def foodPrice():
    # param = request.args.get('p')
    # sample client request params:
    param = {'year':2023, 'month':5, 'latitude':14.604167, 'longitude':120.982222, 'inflation':6.6, 'rice (special)':1, 'Retail':1}
    return str(m.getPrice(param))

if __name__ == "__main__":
    app.run(debug=True)