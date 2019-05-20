class CreateDemandPredictions < ActiveRecord::Migration[5.1]
  def change
    create_table :demand_predictions do |t|
      t.decimal :price
      t.datetime :datetime
      t.string :sector

      t.timestamps
    end
  end
end
