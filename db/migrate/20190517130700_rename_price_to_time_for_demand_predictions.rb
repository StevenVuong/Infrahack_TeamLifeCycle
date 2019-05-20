class RenamePriceToTimeForDemandPredictions < ActiveRecord::Migration[5.1]
  def change
    rename_column :demand_predictions, :price, :value

  end
end
