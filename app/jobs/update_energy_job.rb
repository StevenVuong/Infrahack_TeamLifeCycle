class UpdateEnergyJob < ApplicationJob
  queue_as :default

  def perform(consumption)
    ActionCable.server.broadcast "consumption_channel", message: consumption
  end
end
