class EnergyUpdateChannel < ApplicationCable::Channel
  def subscribed
    # stream_from "some_channel"
    stream_from "consumption_channel"
  end

  def unsubscribed
    # Any cleanup needed when channel is unsubscribed
  end

  def test
    ActionCable.server.broadcast "consumption_channel", message: "woop"
  end
end
