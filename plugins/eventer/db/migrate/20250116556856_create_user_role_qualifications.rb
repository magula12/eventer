class CreateUserRoleQualifications < ActiveRecord::Migration[7.2]
  def change
    create_table :user_role_qualifications do |t|
      t.integer :user_id, null: false
      t.integer :role_id, null: false
      t.integer :category_id, null: false
      t.integer :rating, default: 0, null: false

      t.timestamps
    end

    # Add foreign keys referencing the 'id' column of the respective tables
    add_foreign_key :user_role_qualifications, :users, column: :user_id
    add_foreign_key :user_role_qualifications, :roles, column: :role_id
    add_foreign_key :user_role_qualifications, :issue_categories, column: :category_id
  end
end
