class AddOwnerToVehicle < ActiveRecord::Migration[5.1]
  def change
    add_reference :vehicles, :owner, foreign_key: true
  end
end
