# cs180-group23-project 
An AI and ML-based model that predicts food prices in the Philippines from observed trends in historical data on food prices and the contributing factors using regression analysis

## Jupyter Notebook
The documentation for the model, including the types of regression tested, the parameters tuned, and the training and testing results can be found in the notebook `CS-180-Final-Project.ipynb` in the root folder.

## Dataset
The dataset used in training and testing was retrived from the Humanitarian Data Exchange. The .csv file for the dataset can be found as `wfp_food_prices_phl.csv` in the root folder. This dataset is also publicly available and can be accessed through this [link](https://data.humdata.org/dataset/wfp-food-prices-for-philippines).

## Web App
The predictive model was incorporated into a web application to allow end users to use it as an assistive tool in budgeting and financial decisions.

### Setup
First, create the python virtual environment using the virtualenv module.
``` bash
pip install virtualenv
python -m venv venv
```
In Linux, start the virtual environment by running
``` bash
source ./venv/bin/activate
```
Or, in Windows, by running
``` bash
.\venv\Scripts\activate
```

Next, install the requirements by running
```bash
pip install -r requirements.txt
```

To run the program in debug mode, execute the following command:
``` bash
python -m app.app
```
