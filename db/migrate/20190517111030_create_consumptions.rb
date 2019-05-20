class CreateConsumptions < ActiveRecord::Migration[5.1]
  def change
    create_table :consumptions do |t|
      t.datetime :time
      t.integer :consumption
      t.references :vehicle, foreign_key: true

      t.timestamps
    end
  end
end
