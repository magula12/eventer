module Eventer
  module Hooks
    class ViewMultiAssigneeHook < Redmine::Hook::ViewListener
      render_on :view_issues_form_details_bottom, partial: 'eventer/multi_assignee'
    end
  end
end
