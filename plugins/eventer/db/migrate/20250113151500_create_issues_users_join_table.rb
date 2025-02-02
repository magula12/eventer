class CreateIssuesUsersJoinTable < ActiveRecord::Migration[7.2]
  def change
    create_table :issues_users, id: false do |t|
      t.references :issue, null: false, foreign_key: true
      t.references :user, null: false, foreign_key: true
    end

    add_index :issues_users, [:issue_id, :user_id], unique: true
  end
end
