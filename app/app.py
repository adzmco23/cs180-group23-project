from flask import Flask, request, render_template

from regression import Model

app = Flask(__name__)

m: Model = Model()

# render webpage
@app.get("/")
def hello():
    return render_template('index.html')

# route for calculating food price using regression model
@app.get("/price")
def foodPrice():
    param = request.args.get('p')
    print(param)
    return str(m.getPrice(param))

if __name__ == "__main__":
    app.run(debug=True)