class CustomFilter < ApplicationRecord
  belongs_to :user
  validates :name, presence: true
  validate :valid_conditions_format

  before_save :convert_conditions_to_json

  private

  def convert_conditions_to_json
    return if conditions.is_a?(Hash) # Already a Hash

    parsed_conditions = JSON.parse(conditions) rescue {}
    self.conditions = parsed_conditions if parsed_conditions.is_a?(Hash)
  end

  def valid_conditions_format
    parsed = conditions.is_a?(Hash) ? conditions : (JSON.parse(conditions) rescue nil)
    return errors.add(:conditions, 'nie je platný JSON') unless parsed.is_a?(Hash)

    unless parsed["conditions"].is_a?(Hash) && parsed["rules"].is_a?(Hash)
      errors.add(:conditions, 'Musí obsahovať "rules" a "conditions" ako objekty')
      return
    end
  end
end
