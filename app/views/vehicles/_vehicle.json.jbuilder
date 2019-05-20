json.extract! vehicle, :id, :name, :owner_id, :address, :charging_sector, :battery_capacity, :created_at, :updated_at
json.url vehicle_url(vehicle, format: :json)
