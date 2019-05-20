require 'net/http'

module Backend
    extend ActiveSupport::Concern



        def call_backend
            call = build_call
            
        end 


        def build_call
            call = {'pricePredictions' => PricePrediction.all,
            'demandPredictions' => DemandPrediction.all,
            'maxVehicleChargingRates' => [1,3,4],
            'maxVehicleDischargingRates' => [2,3,4],
            'maxVehicleChargeCapacitites' => [64,32,53],
            'journeyInformation' => [[1,4,8],[2,4,5],[5,6,7]],
            'initialVehicleCharge'=> [5,6,7]
            }
        end
    end
end