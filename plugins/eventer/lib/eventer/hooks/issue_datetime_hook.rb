module Eventer
  module Hooks
    class IssueDatetimeHook < Redmine::Hook::ViewListener
      def view_issues_form_details_top(context = {})
        issue = context[:issue]
        form = context[:form]

        context[:controller].send(:render_to_string, {
          partial: 'issues/datetime_fields',
          locals: { f: form, issue: issue }
        })
      end

      def view_issues_show_description_bottom(context = {})
        issue = context[:issue]

        context[:controller].send(:render_to_string, {
          partial: 'issues/show_datetime',
          locals: { issue: issue }
        })
      end
    end
  end
end
