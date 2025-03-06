# plugins/eventer/lib/eventer/hooks.rb
module Eventer
  module Hooks
    class ViewRoleAssignmentsHook < Redmine::Hook::ViewListener
      # This injects the partial into the bottom of the new/edit issue form
      render_on :view_issues_form_details_bottom,
                partial: 'eventer/role_assignments'
    end
  end
end
