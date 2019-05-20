class Api::V1::ChargedataController < ActionController::API
    
    def index
        render :json => Owner.all
    end

    def submitdata
        params.permit(preferences: {})
        sent_data = data_params
        puts "payload is #{sent_data}"
        render :json => sent_data   
    end


    def data_params
        params.permit(:vehicle_id, :current_capacity, :required_start_time)
    end


end