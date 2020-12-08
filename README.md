# portfol.io









## Data_acquire

The data is from open source library yfinance (Yahoo Finance). For each stock in the portfolio we choose, we set interval to be ‘1m’ to acquire minute level data and drop all columns other than ‘Datetime’ and the close since only the adjusted close will be used. 

Next step is to make a dataframe for the portfolio. We outer merge individual stocks sorted by ‘Datetime’ to preserve all data. On the other hand, doing so would leave us some missing values because yfinance does not provide complete data for each stock. We might use inner merge for prediction as imputing stock price requires carefulness. 

Data_acquire_test has a main loop for continuously updating the collection, which is to upsert the dataframe generated from previous steps. We can set up different download_period to decide how fast we update the collection. Here we update every 10 secs. Whether the update succeeds or returns error messages, it would be recorded in a log file ‘data.log’. The function of setting up a logger lies in ‘utils.py’.

## MongoDB

We create a new M0 cluster on MongoDB to store the data choosing AWS as our cloud provider. We set the connection IP address to all zeros so there’s no limit on users. Anyone can access the database. Connecting to the cluster requires the PyMongo Driver as well as a few dependencies like snappy, gssapi, srv and tls. Once we have them ready, we can modify the connection string driven by Python 3.6 or later and apply it for cluster connection.

## LSTM

Long short-term memory is an artificial recurrent neural network which performs well on time series data. Our idea is to train a LSTM model for either an individual stock or the whole portfolio in real time. Again we are only using close price and datetime. For preprocessing, we will split the data by the ratio of the classic 8:2 and apply MinMaxScaler on the training set. We use 4 hidden layers with 50 neurons running though 100 epochs. We will make predictions using the model just trained. The problem we face now is that the missing value in the portfolio will fail on the scaling and later steps while it’s also hard to impute the stock price. And even so, each epoch would take around 4 secs and the whole process would take about 7 minutes for one stock, which is rather slow compared with the 10 secs update frequency. 
