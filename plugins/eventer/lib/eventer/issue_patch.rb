# plugins/eventer/lib/eventer/issue_patch.rb
module Eventer
  module IssuePatch
    extend ActiveSupport::Concern

    included do
      has_and_belongs_to_many :assigned_users,
                              class_name: 'User',
                              join_table: 'issues_users',
                              foreign_key: 'issue_id',
                              association_foreign_key: 'user_id'
      safe_attributes 'assigned_user_ids'
    end
  end
end

unless Issue.included_modules.include?(Eventer::IssuePatch)
  Issue.send(:include, Eventer::IssuePatch)
end
