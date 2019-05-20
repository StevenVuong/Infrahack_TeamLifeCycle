import mosek
from tools import toAsubAval
import numpy as np
from scipy.sparse import coo_matrix, csc_matrix
from copy import deepcopy

class Optimizer:

	def __init__(self, safetyFactor=1.2, safetyBuffer=0.1):
	    self.safetyFactor = safetyFactor
	    self.safetyBuffer = safetyBuffer # e.g we always want to keep 10% charge in the vehicle at all times

	def Optimize(self,price,nonPEV,max_charging,max_discharging,max_capacity, journeyInformation, initCharge):
		# Work out size of N and T
		N = len(max_charging)
		T = len(price)-1

		# Extract the journey information first
		journeyInformation

		# Initate Q matrix sparse input arrays
		Q_subi = []
		Q_subj = []
		Q_val = []

		# W need to make a Qt matrix for each individual timestep.
		# Then we can add the individuals together to form Q.
		for k in range(T+1):
			Qt = np.ones((N,N))*2*price[k]
			# Now just the lower triangular part of the matrix Qt 
			# is specified using an unordered sparse triplet format
			Qt_lower = np.tril(Qt)
			# Now extract the sparse triplet arrays
			sparse = coo_matrix(Qt_lower)
			qt_subi = sparse.row
			qt_subj = sparse.col
			qt_val = sparse.data

			"""
			The Q matrix contains all Qt matrices in a diagonal form
			therefore if we translate each Qt matrix to its proper
			position we can then just add the matrices to each other
			"""
			qt_subi += k*N
			qt_subj += k*N
			# Now add to Q sparse arrays
			Q_subi += qt_subi.tolist()
			Q_subj += qt_subj.tolist()
			Q_val += qt_val.tolist()

		# Construct the full price array
		price = np.array([k for k in price for a in range(N)])
		# Also contruct the nonPEV in the same way
		nonPEV = np.array([k for k in nonPEV for a in range(N)])
		# Now time to construct the C matrix
		C = np.ones(N*(T+1)) * 2 * price * nonPEV

		"""
		---------------------------------------------------------
		Directly constructing asub and aval. We want the 
		constraints to be dense for every given time step.
		---------------------------------------------------------
		"""

		# Construct asub and aval for all vehicles combines
		asub = [[] for x in range(N*(T+1))]
		aval = [[] for x in range(N*(T+1))]

		for k in range(N*(T+1)):
			vNum = k%N
			tStep = int(np.floor(k/N))
			colSub = (T+1)*(vNum+1)-1-np.arange(T+1-tStep)
			colSub.sort()
			asub[k] += colSub.tolist()
			aval[k] += np.ones(T+1-tStep).tolist()

		"""
		---------------------------------------------------------
		Now time to construct the boundry constraints for the
		journeys.
		---------------------------------------------------------
		"""

		# Find net charge loss and add a safety factor
		net_charge_loss = np.cumsum(journeyInformation*self.safetyFactor, axis=1)

		# Get the lower and higher bounds for charging
		lowerBounds = self.safetyBuffer*max_capacity + net_charge_loss - initCharge
		upperBounds = max_capacity + net_charge_loss - initCharge

		# Stretch bounds out into 1 dimension array of size N*(T+1)
		lowerBounds = lowerBounds.flatten()
		upperBounds = upperBounds.flatten()

		"""
		---------------------------------------------------------
		In this section we will prepare the system variable bounds
		---------------------------------------------------------
		"""
		vehiclesTraveling = journeyInformation.flatten()
		vehiclesTraveling[vehiclesTraveling > 0] = 1
		vehiclesTraveling = 1 - vehiclesTraveling

		bval_variables_lower = np.tile(max_discharging,T+1)*vehiclesTraveling
		bval_variables_upper = np.tile(max_charging,T+1)*vehiclesTraveling
		bval_variables_lower = bval_variables_lower.tolist()
		bval_variables_upper = bval_variables_upper.tolist()

		"""
		-----------------------------------------------------------
		Now we are finally ready to start the optimisation process!
		We will create a mosek task in a mosek environment and then
		insert all necessary components as needed
		-----------------------------------------------------------
		"""

		# Worth logging this server side for debugging scenarios etc
		def printVar(var, varname):
			print("{} = {}".format(varname, var))

		printVar(price, "Price")
		printVar(nonPEV, "nonPEV")
		printVar(lowerBounds, "Lower bounds")
		printVar(upperBounds, "Upper bounds")
		printVar(C, "C")
		printVar(asub, "asub")

		with mosek.Env() as env:
			with env.Task() as task:

				# Set how many variables and contraints you are using
				task.appendvars(N*(T+1))
				task.appendcons(len(lowerBounds))
				
				# Lets now set the objective up
				task.putqobj(Q_subi, Q_subj, Q_val)
				task.putobjsense(mosek.objsense.minimize)
				for j in range(N*(T+1)):
					
					# Puting down C vals
					task.putcj(j, C[j])

					# Now to set up the constraint coefficients
					task.putacol(j,asub[j],aval[j])

					# Now set up the bounds for the system variables.
					if bval_variables_upper[j] == 0:
						task.putvarbound(j, mosek.boundkey.fx, bval_variables_lower[j], bval_variables_upper[j])
					else:
						task.putvarbound(j, mosek.boundkey.ra, bval_variables_lower[j], bval_variables_upper[j])

					# Also set the bounds for the constraints in the system
					task.putconbound(j, mosek.boundkey.ra, lowerBounds[j], upperBounds[j]) 

				# Now we have set up fully we can now run the optimisation!
				print('Setup is now complete, optimisation will now start\n')
				task.optimize()
				print('Optimisation has now finished. Now extracting solution..\n')

				# Extract X and reshape to an array with dimension NxT
				X = [0.] * N * (T+1)
				task.getxx(mosek.soltype.itr, X)
				X = np.reshape(np.array(X), (N,(T+1)), order=1)

		# We can now return the charging profiles as they are :)
		return X

	def dumbOptimize(self,max_charging,max_capacity,journeyInformation,initCharge):
		net_charge_loss = np.cumsum(journeyInformation, axis=1)

		# Validate the data
		T = len(journeyInformation[0])-1
		N = len(max_charging)

		chargeProfile = np.zeros((N,T+1))
		for k in range(N):
			vehicleProfile = journeyInformation[k,:]
			lossProfile = net_charge_loss[k,:]
			
			vMaxCharge = max_charging[k]
			vMaxCapacity = max_capacity[k]

			travelingStatus = journeyInformation[k,:]
			travelingStatus[travelingStatus > 0] = 1

			vCharge = initCharge[k]
			for t in range(T+1):
				if travelingStatus[t]:
					vCharge -= vehicleProfile[t]
				else:
					# Work out how much to charge in this time period
					refilVal = vMaxCapacity - vCharge
					if refilVal > vMaxCharge:
						refilVal = vMaxCharge
					# Update charging details
					vCharge += refilVal
					chargeProfile[k,t] = refilVal

		# This should be acceptable now
		return chargeProfile
