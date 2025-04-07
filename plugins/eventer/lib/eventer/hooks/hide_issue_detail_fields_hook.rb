module Eventer
  module Hooks
    class HideIssueDetailFieldsHook < Redmine::Hook::ViewListener
      # This hook places content at the bottom of the main issue details area
      render_on :view_issues_show_details_bottom, partial: 'eventer/hide_issue_details'
    end
  end
end