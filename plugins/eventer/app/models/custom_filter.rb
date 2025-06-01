#plugins/eventer/app/models/custom_filter.rb
class CustomFilter < ApplicationRecord
  belongs_to :user
  validates :name, presence: true
  validate :valid_conditions_format
  before_save :convert_conditions_to_json

  private
  def convert_conditions_to_json
    return if conditions.is_a?(Hash)

    parsed_conditions = JSON.parse(conditions) rescue {}
    self.conditions = parsed_conditions if parsed_conditions.is_a?(Hash)
  end

  def valid_conditions_format
    parsed = conditions.is_a?(Hash) ? conditions : (JSON.parse(conditions) rescue nil)
    return errors.add(:conditions, I18n.t('errors.invalid_json')) unless parsed.is_a?(Hash)

    unless parsed["conditions"].is_a?(Hash) && parsed["rules"].is_a?(Hash)
      errors.add(:conditions, I18n.t('errors.missing_conditions_and_rules'))
      return
    end
  end
end