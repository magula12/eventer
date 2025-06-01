class CreateUserRoleQualifications < ActiveRecord::Migration[7.2]
  def change
    create_table :user_role_qualifications do |t|
      t.integer :user_id, null: false
      t.integer :role_id, null: false
      t.integer :category_id, null: false
      t.integer :rating, default: 0, null: false

      t.timestamps
    end

    add_foreign_key :user_role_qualifications, :users, column: :user_id
    add_foreign_key :user_role_qualifications, :roles, column: :role_id
    add_foreign_key :user_role_qualifications, :issue_categories, column: :category_id

    add_index :user_role_qualifications, [:user_id, :role_id, :category_id], unique: true, name: 'index_unique_user_role_category'
  end
end
