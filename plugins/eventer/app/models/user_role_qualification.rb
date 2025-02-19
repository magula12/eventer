class UserRoleQualification < ApplicationRecord
  belongs_to :user
  belongs_to :role
  belongs_to :category, class_name: 'IssueCategory', foreign_key: 'category_id'
end