class Consumption < ApplicationRecord
  belongs_to :vehicle
  after_commit { UpdateEnergyJob.perform_later(self) }
end
