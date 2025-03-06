module Eventer
  module IssuePatch
    extend ActiveSupport::Concern

    included do
      has_and_belongs_to_many :assigned_users,
                              class_name: 'User',
                              join_table: 'issues_users',
                              foreign_key: 'issue_id',
                              association_foreign_key: 'user_id'

      has_many :issue_role_assignments, dependent: :destroy
      accepts_nested_attributes_for :issue_role_assignments, allow_destroy: true

      safe_attributes 'assigned_user_ids', 'start_datetime'

      # Override assigned_to to return multiple users
      def assigned_to
        assigned_users.first # Redmine expects a single user, so return the first one
      end

      def assigned_to=(user)
        self.assigned_users = if user.is_a?(User)
                                [user] # Set single user assignment
                              else
                                User.where(id: user) # Set multiple users
                              end
      end

      # Ensure start_datetime is required
      validates :start_datetime, presence: true
    end
  end
end

# Apply patch
unless Issue.included_modules.include?(Eventer::IssuePatch)
  Issue.send(:include, Eventer::IssuePatch)
end
