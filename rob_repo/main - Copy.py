import flask
from flask import request, jsonify
from optimizer import Optimizer
from predictor import DemandPredictor
from werkzeug.exceptions import BadRequest
import numpy as np
import json

# Setup flask server config
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Setup optimizer and predictor
optimizer = Optimizer(1,0)
demandPredictor = DemandPredictor()

@app.route('/api/GetChargingProfile', methods=['GET', 'POST'])
def home():

	# Get the data
	data = request.data
	data = json.loads(data)

	# Extract all necessary variables
	try:
		print(type(data["pricePredictions"]))
		price = np.array(data["pricePredictions"])
		nonPEV = np.array(data["demandPredictions"])
		max_charging = np.array(data["maxVehicleChargingRates"])
		max_discharging = np.array(data["maxVehicleDischargingRates"])
		max_capacity = np.array(data["maxVehicleChargeCapacities"])
		journeyInformation = np.array(data["journeyInformation"])
		initCharge = np.array(data["initialVehicleCharge"])
	except Exception as e:
		raise BadRequest('Was not able to deserialise the data!!\n\n {}\n\n\nRequest={}'.format(e,data))

	# Validate the data
	T = len(price)-1
	N = len(max_charging)

	if len(max_discharging)!=N or len(max_capacity)!=N or len(initCharge)!=N:
		raise BadRequest('Size of N is not consistant!!')
	if len(nonPEV)!=T+1:
		raise BadRequest('Size of T is not consistant!!')
	if journeyInformation.shape != (N,T+1):
		raise BadRequest('Size of journeyInformation matrix is not correct!!')

	# Run the optimisation to get the charging profiles
	smartChargingProfiles = optimizer.Optimize(price,nonPEV,max_charging,max_discharging,max_capacity,journeyInformation,initCharge)
	smartChargingProfiles = np.round(smartChargingProfiles,2)

	# Run to get the dumb charging profiles also
	dumbChargingProfiles = optimizer.dumbOptimize(max_charging,max_capacity,journeyInformation,initCharge)
	dumbChargingProfiles = np.round(dumbChargingProfiles,2)

	# Extra infered summary details
	combinedSmartCharging = smartChargingProfiles.sum(axis=0)
	combinedDumbCharging = dumbChargingProfiles.sum(axis=0)
	
	# Lets also get the combined charge requirement
	totalSmartDemand = combinedSmartCharging + nonPEV
	totalDumbDemand = combinedDumbCharging + nonPEV

	# Lets also keep a running total of how much charge each vehicle is storing
	net_charge_loss = np.cumsum(journeyInformation, axis=1) # Don't include safety factor here
	smartVehicleCharge = np.cumsum(smartChargingProfiles,axis=1)+initCharge[:,np.newaxis]
	smartVehicleCharge = smartVehicleCharge - net_charge_loss
	dumbVehicleCharge = np.cumsum(dumbChargingProfiles,axis=1)+initCharge[:,np.newaxis]
	dumbVehicleCharge = dumbVehicleCharge - net_charge_loss

	# smart and dumb charging cost comparison
	smartCost = np.sum(price*(nonPEV+smartVehicleCharge)**2)
	dumbCost = np.sum(price*(nonPEV+dumbVehicleCharge)**2)
	smartSavings = (1-smartCost/dumbCost)*100 # This will be a percentage saving

	# Finally return all the necessary information
	data = {}
	data['smartCost'] = smartCost
	data['dumbCost'] = dumbCost
	data['smartSavings'] = smartSavings
	data['smartChargingProfiles'] = smartChargingProfiles.tolist()
	data['dumbChargingProfiles'] = dumbChargingProfiles.tolist()
	data['combinedSmartCharging'] = combinedSmartCharging.tolist()
	data['combinedDumbCharging'] = combinedDumbCharging.tolist()
	data['totalSmartDemand'] = totalSmartDemand.tolist()
	data['totalDumbDemand'] = totalDumbDemand.tolist()
	json_data = json.dumps(data)

	response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json')
	return response

@app.route('/api/GetDemandPredictions', methods=['GET', 'POST'])
def getPredictions():
	prediction = demandPredictor.Predict("model")
	response = app.response_class(
        response=json.dumps(prediction),
        status=200,
        mimetype='application/json')
	return response

app.run()