class AddDatetimeFieldsToIssues < ActiveRecord::Migration[7.2]
  def change
    add_column :issues, :start_datetime, :datetime
    add_column :issues, :end_datetime, :datetime
  end
end
