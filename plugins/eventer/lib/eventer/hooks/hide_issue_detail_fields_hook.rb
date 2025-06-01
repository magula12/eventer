module Eventer
  module Hooks
    class HideIssueDetailFieldsHook < Redmine::Hook::ViewListener
      render_on :view_issues_show_details_bottom, partial: 'eventer/hide_issue_details'
    end
  end
end