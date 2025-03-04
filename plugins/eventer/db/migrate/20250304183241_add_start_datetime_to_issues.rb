class AddStartDatetimeToIssues < ActiveRecord::Migration[7.2]
  def change
    add_column :issues, :start_datetime, :datetime
  end
end
