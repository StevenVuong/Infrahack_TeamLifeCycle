import fbprophet
from fbprophet import Prophet
import pickle
import pandas as pd
import matplotlib.pyplot as plt

class DemandPredictor:
	def __init__(self):
		print("Starting predictor")

	def Train(self,months,modelPath):

		# function to import raw data
		def import_data(url):
			df = pd.read_csv(url)
			return df
  		# import data
		gridwatch_df = import_data("gridwatch.csv")

		# change the labels
		gridwatch_df = gridwatch_df.rename(columns={' timestamp':'ds', ' demand':'y'})
		gridwatch_df.head()

		# More formatting
		gridwatch_df.y = gridwatch_df.y.astype(int)

		# turn strings into datetime
		gridwatch_df['ds'] = pd.to_datetime(gridwatch_df.iloc[:,0], format='%Y-%m-%d %H:%M:%S')
		length = len(gridwatch_df)

		# Get all the needed time data
		trainingTime = length - (6*24*30*months)
		df2 = gridwatch_df[trainingTime:]
		df2.reset_index(inplace=True)
		df2.tail()
		df2['cap'] = 55000
		df2['floor'] = 15000

		# Construct model
		prophet = Prophet( changepoint_prior_scale=0.10, growth='logistic')
		prophet.add_country_holidays(country_name='UK')
		prophet.fit(df2)

		# Save the model
		with open(modelPath, "wb") as f:
			pickle.dump(prophet, f)

	def Predict(self, forcasterPath, hours_predicted):
		# Load the prophet
		with open(forcasterPath, "rb") as f:
			prophet = pickle.load(f)

		# These are already pre-loaded
		# future = prophet.make_future_dataframe(periods=hours_predicted, freq='H')
		# future['cap'] = 55000
		# future['floor'] = 15000
		# future.tail()

		# load the forecaster
		with open("trained_forecast11", "rb") as f:
			forecast = pickle.load(f)

		# forecast uncertainty for future predicted points
		forecast = prophet.predict(future)
		forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head()

		prophet.plot(forecast, xlabel='date', ylabel='consumption(kWH)')
		prophet.plot_components(forecast)

		# print(forecast)
		return forecast.yhat