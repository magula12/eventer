module Eventer
  module Hooks
    class IssueRoleAssignmentHook < Redmine::Hook::Listener
      def controller_issues_new_after_save(context = {})
        issue = context[:issue]
        params = context[:params]
        role_assignments = params.dig(:issue, :role_assignments)
        return unless role_assignments

        build_role_assignments_for_issue(issue, role_assignments)
      end


      def controller_issues_edit_before_save(context = {})
        issue = context[:issue]
        params = context[:params]
        role_assignments = params.dig(:issue, :role_assignments)
        return unless role_assignments

        # Update existing or rebuild them
        issue.issue_role_assignments.destroy_all
        build_role_assignments_for_issue(issue, role_assignments)
      end

      private

      def build_role_assignments_for_issue(issue, role_assignments_param)
        role_assignments_param.each do |_index, ra_params|
          IssueRoleAssignment.create!(
            issue_id: issue.id,
            role_id: ra_params[:role_id],
            required_count: ra_params[:required_count],
            assigned_user_ids: (ra_params[:assigned_user_ids] || []).reject(&:blank?)
          )
        end
      end
    end
  end
end
