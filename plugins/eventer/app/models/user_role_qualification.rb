class UserRoleQualification < ApplicationRecord
  belongs_to :user
  belongs_to :role
  belongs_to :category, class_name: 'IssueCategory', foreign_key: 'category_id'

  # Validate that rating is an integer between 0 and 10.
  validates :rating, numericality: { only_integer: true, greater_than_or_equal_to: 0, less_than_or_equal_to: 10 }
end
