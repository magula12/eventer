class CustomFilter < ApplicationRecord
  belongs_to :user
  validates :name, presence: true

  validate :valid_json_conditions

  private

  def valid_json_conditions
    JSON.parse(conditions)
  rescue JSON::ParserError
    errors.add(:conditions, 'nie je platný JSON formát')
  end
end
