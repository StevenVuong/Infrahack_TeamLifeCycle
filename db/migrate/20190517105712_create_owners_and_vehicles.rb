class CreateOwnersAndVehicles < ActiveRecord::Migration[5.1]
  def change
    create_table :vehicles do |t|
      t.string :name
      t.string :address
      t.string :charging_sector
      t.integer :battery_capacity

      t.timestamps
  end
    create_table :owners do |t|
      t.string :name
      t.references :vehicle, foreign_key: true

      t.timestamps


    end
      
  end
end
