class CreateOffDays < ActiveRecord::Migration[7.2]
  def change
    create_table :off_days do |t|
      t.references :user, null: false, foreign_key: true  # Adding reference to user
      t.datetime :start_datetime
      t.datetime :end_datetime

      t.timestamps
    end
  end
end
