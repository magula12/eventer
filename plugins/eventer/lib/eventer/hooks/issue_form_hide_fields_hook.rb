# lib/hooks/issue_form_hide_fields_hook.rb
module Eventer
  module Hooks
    class IssueFormHideFieldsHook < Redmine::Hook::ViewListener
      render_on :view_issues_form_details_bottom, partial: 'eventer/hide_issue_fields'
    end
  end
end
