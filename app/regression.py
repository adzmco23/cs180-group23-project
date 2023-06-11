import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.preprocessing import MinMaxScaler

class Model:
    def __init__(self):
        #import the self.dataset
        self.data = pd.read_csv('wfp_food_prices_phl.csv')

        #Change the datatype of date and get the year and month
        #Add a year and month column which will be used for our regression model
        self.data['date'] = self.data['date'].astype('datetime64[ns]')
        self.data['year'] = self.data['date'].dt.year
        self.data['month'] = self.data['date'].dt.month

        #Drop all the null values and the rows with price == 0 
        #since there are null or 0 price in the dataset
        #We need to remove them because those are incomplete data
        self.data.dropna(inplace= True)
        self.data.drop(self.data.loc[self.data['price']==0].index, inplace=True)

        #Drop the unnecessary columns from the self.dataset
        self.data = self.data.drop(['date', 'admin1','admin2','market','category', 'currency', 'unit'
                ,'usdprice'], axis='columns')

        #Get dummy values for the categorical columns
        self.data = pd.get_dummies(data=self.data)

        self.data['month2'] = self.data['month']**2 # add degree of freedom
        self.data['longlat'] = self.data['longitude']*self.data['latitude'] # long-lat relationship
        self.data['inflyr'] = self.data['year']*self.data['inflation'] # inflation-year relationship
        self.data['locyr'] = self.data['inflyr']*self.data['longlat'] # location-year relationship
        self.data['locmth'] = self.data['month']*self.data['month2']*self.data['longlat'] # location-month relationship

        #divide the self.data into test and training sets
        X = self.data.drop(['price'], axis='columns')
        y = self.data['price'].values
        
        # normalize non-dummy columns using MinMaxScaler
        self.sc = MinMaxScaler()
        X[['latitude','longitude','inflation','year','month','month2','longlat','inflyr','locyr','locmth']] = self.sc.fit_transform(X[['latitude','longitude','inflation','year','month','month2','longlat','inflyr','locyr','locmth']])


        # For each commodity, add a new interaction feature with each of the non-commodity predictors in the dataset
        for i in X.columns:
            if i not in ['inflation','year','inflyr','longlat','latitude','longitude','locyr','locmth','month','month2','location','priceflag_actual','priceflag_actual,aggregate','priceflag_aggregate','pricetype_Farm Gate','pricetype_Retail','pricetype_Wholesale']:
                for j in ['year','inflyr','locyr','locmth','latitude','longitude','longlat','month','month2','priceflag_actual','priceflag_actual,aggregate','priceflag_aggregate','pricetype_Farm Gate','pricetype_Retail','pricetype_Wholesale']:
                    X.insert(len(X.columns),i+' x '+j,X[i]*X[j])
                    #X=pd.concat((X,(X[i]*X[j]).rename(i+j)),axis=1)

        # remove commodity-dependent presictors
        X = X.drop(['month','month2','locmth','priceflag_actual','priceflag_actual,aggregate','priceflag_aggregate','pricetype_Farm Gate','pricetype_Retail','pricetype_Wholesale'], axis='columns')
                    
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=26)

        #Train the model using the training set

        self.regressor = Ridge(alpha=0.01)
        self.regressor.fit(X_train, y_train)
    
    def getPrice(self, params):
        d = pd.DataFrame(data=None, columns=self.data.drop(['price'], axis='columns').columns)
        '''
        only a subset of possible inputs were implemented for the demonstration

        commodities considered: rice (regular), rice (special), eggs, mango, chicken
        locations considered (latlong mappings): region 1 (Ilocos Norte), Metro Manila, region 6 (Iloilo), region 8 (southern leyte), region 10 (Lanao del Norte)
        priceflag: actual only
        pricetype: retail or wholesale

        '''
        
        d = d.append({'year':params['year'],'month':params['month'], 'latitude':params['latitude'],
                      'longitude':params['longitude'], 'inflation':params['inflation'],
                      'commodity_Mangoes (carabao)':params.setdefault('mango',0), 'commodity_Rice (regular, milled)':params.setdefault('rice (regular)',0),
                      'commodity_Rice (special)':params.setdefault('rice (special)',0), 'commodity_Eggs':params.setdefault('eggs',0),
                      'commodity_Meat (chicken, whole)':params.setdefault('chicken',0),
                      'priceflag_actual':1, 'pricetype_Retail':params.setdefault('retail',0),
                      'pricetype_Wholesale':params.setdefault('wholesale',0)}, ignore_index=True)
        
        ### PREPROCESS TO MATCH DF FORMAT

        d = d.fillna(0)
        d['month2'] = d['month']**2 # add degree of freedom
        d['longlat'] = d['longitude']*d['latitude'] # long-lat relationship
        d['inflyr'] = d['year']*d['inflation'] # inflation-year relationship
        d['locyr'] = d['inflyr']*d['longlat'] # location-year relationship
        d['locmth'] = d['month']*d['month2']*d['longlat'] # location-month relationship

        d[['latitude','longitude','inflation','year','month','month2','longlat','inflyr','locyr','locmth']] = self.sc.transform(d[['latitude','longitude','inflation','year','month','month2','longlat','inflyr','locyr','locmth']])

        # For each commodity, add a new interaction feature with each of the non-commodity predictors in the dataset
        for i in d.columns:
            if i not in ['inflation','year','inflyr','longlat','latitude','longitude','locyr','locmth','month','month2','location','priceflag_actual','priceflag_actual,aggregate','priceflag_aggregate','pricetype_Farm Gate','pricetype_Retail','pricetype_Wholesale']:
                for j in ['year','inflyr','locyr','locmth','latitude','longitude','longlat','month','month2','priceflag_actual','priceflag_actual,aggregate','priceflag_aggregate','pricetype_Farm Gate','pricetype_Retail','pricetype_Wholesale']:
                    d.insert(len(d.columns),i+' x '+j,d[i]*d[j])
                    #X=pd.concat((X,(X[i]*X[j]).rename(i+j)),axis=1)

        # remove commodity-dependent presictors
        d = d.drop(['month','month2','locmth','priceflag_actual','priceflag_actual,aggregate','priceflag_aggregate','pricetype_Farm Gate','pricetype_Retail','pricetype_Wholesale'], axis='columns')

        print(params)
        params.update({'price': self.regressor.predict(d)[0]})
        return params