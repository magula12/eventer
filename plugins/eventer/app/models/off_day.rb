#plugins/eventer/app/models/off_day.rb
class OffDay < ApplicationRecord
  belongs_to :user

  validates :start_datetime, presence: true
  validates :end_datetime, presence: true
end
