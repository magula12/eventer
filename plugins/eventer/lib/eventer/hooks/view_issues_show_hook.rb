module Eventer
  module Hooks
    class ViewIssuesShowHook < Redmine::Hook::ViewListener
      def view_issues_show_details_bottom(context = {})
        issue = context[:issue]
        return '' if issue.assigned_users.empty?

        users_list = issue.assigned_users.map { |u| link_to(u.name, user_path(u)) }.join(', ').html_safe

        "<p><strong>#{l(:field_assigned_users)}:</strong> #{users_list}</p>".html_safe
      end
    end
  end
end
