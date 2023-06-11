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

    # get request parameters
    req = request.args.to_dict()
    year = int(req.setdefault('year',2023))
    month = int(req.setdefault('month',5))
    commodity = req.setdefault('commodity','eggs')
    pricetype = req.setdefault('pricetype','retail')
    inflation = int(req.setdefault('inflation',6.6))
    location = req.setdefault('location','Metro Manila')

    # latitude-longitude mapping
    latlong = {
        'Region 1 (Ilocos Norte)':(18.194082,120.595955),
        'Metro Manila':(14.604167, 120.982222), 
        'region 6 (Iloilo)':(10.696944,122.564444), 
        'region 8 (southern leyte)':(10.136111,125.005), 
        'region 10 (Lanao del Norte)':(8.219167,124.248889)
    }
    
    latitude = latlong[location][0]
    longitude = latlong[location][1]

    param = {'year':year, 'month': month, 'latitude':latitude, 'longitude':longitude, 'inflation':inflation}
    param.update({commodity: 1})
    param.update({pricetype: 1})

    print(param)

    # predict price using getPrice() of class Model in regression.py
    return str(m.getPrice(param))

if __name__ == "__main__":
    app.run(debug=True)