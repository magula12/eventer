module Eventer
  module IssueHelperPatch
    def self.included(base)
      base.class_eval do
        alias_method :original_issue_assigned_to_details, :issue_assigned_to_details

        def issue_assigned_to_details(issue)
          if issue.assigned_users.any?
            issue.assigned_users.map { |u| link_to u.name, user_path(u) }.join(', ').html_safe
          else
            original_issue_assigned_to_details(issue)
          end
        end
      end
    end
  end
end

# unless IssuesHelper.included_modules.include?(Eventer::IssueHelperPatch)
#   IssuesHelper.send(:include, Eventer::IssueHelperPatch)
#   Rails.logger.info 'Eventer::IssuesControllerPatch included'
# end
