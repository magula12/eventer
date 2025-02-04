class CustomFilter < ApplicationRecord
  belongs_to :user
  validates :name, presence: true
  validate :valid_conditions_format

  before_save :convert_conditions_to_json

  private

  def convert_conditions_to_json
    return if conditions.is_a?(Hash) # Už je JSON

    self.conditions = JSON.parse(conditions) rescue nil
  end

  def valid_conditions_format
    parsed = JSON.parse(conditions) rescue nil
    return errors.add(:conditions, 'nie je platný JSON') unless parsed.is_a?(Hash)

    unless parsed.key?("rules")
      errors.add(:conditions, 'chýba kľúč "rules"')
      return
    end

    # Overíme správnosť operátorov v podmienkach
    validate_condition_rules(parsed["conditions"], "Conditions") if parsed["conditions"]
    validate_condition_rules(parsed["rules"], "Rules")
  end

  def validate_condition_rules(rules, type)
    valid_operators = ["==", "!=", ">", "<", ">=", "<=", "in", "not in"]

    rules.each do |key, condition|
      unless condition.is_a?(Hash) && condition.keys.all? { |op| valid_operators.include?(op) }
        errors.add(:conditions, "#{type} obsahuje neplatnú podmienku: #{key} => #{condition}")
      end
    end
  end
end
