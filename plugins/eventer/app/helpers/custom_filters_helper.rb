#plugins/eventer/app/helpers/custom_filters_helper.rb
module CustomFiltersHelper
  def readable_conditions(conditions)
    return I18n.t('helper.no_conditions') if conditions.blank?

    parsed_conditions = conditions.is_a?(String) ? JSON.parse(conditions) : conditions
    readable_text = []

    if parsed_conditions["conditions"]
      readable_text << format_logic(parsed_conditions["conditions"], I18n.t('helper.conditions'))
    end

    if parsed_conditions["rules"]
      readable_text << format_logic(parsed_conditions["rules"], I18n.t('helper.rules'))
    end

    readable_text.join(" | ")
  rescue JSON::ParserError
    I18n.t('helper.invalid_data')
  end

  private

  def format_logic(logic_block, label)
    logic_type = logic_block.keys.first # "and" or "or"
    conditions = logic_block[logic_type]

    return "#{label}: #{I18n.t('helper.no_conditions')}" if conditions.blank?

    formatted_conditions = conditions.map do |condition|
      format_condition(condition)
    end.join(" #{logic_type.upcase} ")

    "#{label}: (#{formatted_conditions})"
  end

  def format_condition(condition)
    return "" unless condition.is_a?(Hash)

    operator, values = condition.first
    return "(#{I18n.t('helper.unknown_condition')})" if values.nil? || !values.is_a?(Array) || values.empty?

    variable = values[0]
    value = values[1] || "(#{I18n.t('helper.unknown_value')})"

    variable_name = variable.is_a?(Hash) ? variable.dig("var")&.split(".")&.last&.capitalize : variable.to_s

    operator_text = operator_to_text(operator)

    " #{value} #{operator_text} #{variable_name}"
  end

  def operator_to_text(operator)
    {
      "==" => I18n.t('operator.equals'),
      "!=" => I18n.t('operator.not_equals'),
      ">" => I18n.t('operator.greater_than'),
      "<" => I18n.t('operator.less_than'),
      ">=" => I18n.t('operator.greater_or_equal'),
      "<=" => I18n.t('operator.less_or_equal'),
      "in" => I18n.t('operator.contains'),
      "not in" => I18n.t('operator.not_contains')
    }[operator] || operator
  end
end