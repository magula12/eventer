module Eventer
  module Hooks
    class ViewIssueRolesShowHook < Redmine::Hook::ViewListener
      # Use render_on for the same hook name, but partial-based
      render_on :view_issues_show_details_bottom, partial: 'eventer/role_assignment_display'
    end
  end
end
