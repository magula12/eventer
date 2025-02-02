module Eventer
  module IssuePatch
    extend ActiveSupport::Concern

    included do
      has_and_belongs_to_many :assigned_users, class_name: 'User', join_table: 'issues_users', foreign_key: 'issue_id', association_foreign_key: 'user_id'

      # Other code for your plugin (if any)
    end
    #new code here
  end
end
