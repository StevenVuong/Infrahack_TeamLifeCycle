from predictor import DemandPredictor

demandPredictor = DemandPredictor()

# output = demandPredictor.Train(1, "model")
output = demandPredictor.Predict("trained_model11", 24)

print(output)