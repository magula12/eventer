module Eventer
  module Hooks
    class ViewIssueRolesShowHook < Redmine::Hook::ViewListener
      render_on :view_issues_show_details_bottom, partial: 'eventer/role_assignment_display'
    end
  end
end
