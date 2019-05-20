class AddLatitudeandLongitudeToVehicle < ActiveRecord::Migration[5.1]
  def change
    add_column :vehicles, :latitude, :decimal
    add_column :vehicles, :longitude, :decimal

  end
end
