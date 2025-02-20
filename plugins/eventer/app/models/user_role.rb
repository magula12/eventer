class UserRole < ApplicationRecord
  belongs_to :user
  belongs_to :role


  validates :rating, numericality: { only_integer: true, greater_than_or_equal_to: 0, less_than_or_equal_to: 10 }, allow_nil: true
end
