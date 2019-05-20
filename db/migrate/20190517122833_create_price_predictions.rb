class CreatePricePredictions < ActiveRecord::Migration[5.1]
  def change
    create_table :price_predictions do |t|
      t.decimal :price
      t.datetime :datetime
      t.string :sector

      t.timestamps
    end
  end
end
