class API::V1::ConsumptionController < ActionController::API
    
    def create
        @consumption = Consumption.new(consumption_params)
        if @consumption.save
            return render :json => @consumption
        end
        head 400
    end

    def consumption_params
        params.permit(:time, :consumption, :vehicle_id)
    end


end