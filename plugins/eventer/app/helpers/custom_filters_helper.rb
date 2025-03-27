module CustomFiltersHelper
  def readable_conditions(conditions)
    return "Žiadne podmienky" if conditions.blank?

    parsed_conditions = conditions.is_a?(String) ? JSON.parse(conditions) : conditions
    readable_text = []

    # Convert conditions and rules separately
    if parsed_conditions["conditions"]
      readable_text << format_logic(parsed_conditions["conditions"], "Podmienky")
    end

    if parsed_conditions["rules"]
      readable_text << format_logic(parsed_conditions["rules"], "Pravidlá")
    end

    readable_text.join(" | ") # Join conditions and rules with separator
  rescue JSON::ParserError
    "Neplatné dáta"
  end

  private

  def format_logic(logic_block, label)
    logic_type = logic_block.keys.first # "and" or "or"
    conditions = logic_block[logic_type]

    return "#{label}: Žiadne" if conditions.blank?

    formatted_conditions = conditions.map do |condition|
      format_condition(condition)
    end.join(" #{logic_type.upcase} ")

    "#{label}: (#{formatted_conditions})"
  end

  def format_condition(condition)
    return "" unless condition.is_a?(Hash)

    operator, values = condition.first
    return "(Neznáma podmienka)" if values.nil? || !values.is_a?(Array) || values.empty?

    variable = values[0]  # First item in the array should be the variable
    value = values[1] || "(neznáma hodnota)" # Default to '?' if missing

    # Safely extract the variable name
    variable_name = variable.is_a?(Hash) ? variable.dig("var")&.split(".")&.last&.capitalize : variable.to_s

    operator_text = operator_to_text(operator)

    " #{value} #{operator_text} #{variable_name}"
  end

  def operator_to_text(operator)
    {
      "==" => "je",
      "!=" => "nie je",
      ">" => "je väčšie ako",
      "<" => "je menšie ako",
      ">=" => "je väčšie alebo rovné",
      "<=" => "je menšie alebo rovné",
      "in" => "obsahuje",
      "not in" => "neobsahuje"
    }[operator] || operator
  end
end
