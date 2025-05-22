# plugins/eventer/app/models/issue_role_assignment.rb
class IssueRoleAssignment < ActiveRecord::Base
  belongs_to :issue
  belongs_to :role
  validates :role_id, :required_count, presence: true
  validates :required_count, numericality: { greater_than_or_equal_to: 1 }

  # Ensure assigned_user_ids is an array of integers
  before_save :normalize_assigned_user_ids

  private

  def normalize_assigned_user_ids
    self.assigned_user_ids = (assigned_user_ids || []).map(&:to_i).uniq.reject(&:zero?)
  end
end