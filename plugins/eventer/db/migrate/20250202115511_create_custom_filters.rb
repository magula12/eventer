class CreateCustomFilters < ActiveRecord::Migration[7.2]
  def change
    create_table :custom_filters do |t|
      t.references :user, null: false, foreign_key: true
      t.string :name, null: false
      t.text :conditions, default: {}

      t.timestamps
    end
  end
end
