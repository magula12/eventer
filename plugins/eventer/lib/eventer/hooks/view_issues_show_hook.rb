# plugins/eventer/lib/eventer/hooks/view_issues_show_hook.rb
module Eventer
  module Hooks
    class ViewIssuesShowHook < Redmine::Hook::ViewListener
      def view_issues_show_details_bottom(context = {})
        issue = context[:issue]
        return '' if issue.assigned_user_ids.empty?

        users = User.where(id: issue.assigned_user_ids).to_a
        users_list = users.map { |u| link_to(u.name, user_path(u)) }.join(', ').html_safe

        "<p><strong>#{l(:field_assigned_users)}:</strong> #{users_list}</p>".html_safe
      end
    end
  end
end