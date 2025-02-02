class AddPriorityCol < ActiveRecord::Migration[7.2]
  def change
    add_column :issue_categories, :priority, :integer
  end
end
