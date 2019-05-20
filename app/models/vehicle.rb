class Vehicle < ApplicationRecord
  belongs_to :owner
  has_many :consumptions
end
