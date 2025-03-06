class CreateIssueRoleAssignments < ActiveRecord::Migration[7.2]
  def change
    create_table :issue_role_assignments do |t|
      t.references :issue, null: false, foreign_key: true
      t.integer :role_id, null: false
      t.integer :required_count, null: false, default: 1
      t.text :assigned_user_ids, array: true, default: []

      t.timestamps
    end
  end
end