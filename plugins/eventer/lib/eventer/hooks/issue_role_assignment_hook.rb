#TODO: Check if it works properly
module Eventer
  module Hooks
    class IssueRoleAssignmentHook < Redmine::Hook::Listener
      def controller_issues_new_after_save(context = {})
        #Rails.logger.info "[Eventer] RoleAssignmentHook (new_after_save) triggered"
        issue = context[:issue]
        params = context[:params]
        role_assignments = params.dig(:issue, :role_assignments)
        return if role_assignments.blank?

        issue.issue_role_assignments.destroy_all
        build_role_assignments_for_issue(issue, role_assignments)

        issue.issue_role_assignments.reload

        all_assigned_ids = issue.issue_role_assignments
                                .map(&:assigned_user_ids)
                                .flatten
                                .uniq
        #Rails.logger.info "[Eventer] Overwriting assigned_user_ids with role-based: #{all_assigned_ids.inspect}"
        issue.assigned_user_ids = all_assigned_ids
      end

      def controller_issues_edit_before_save(context = {})
        #Rails.logger.info "[Eventer] RoleAssignmentHook (edit_before_save) triggered"
        issue = context[:issue]
        params = context[:params]
        role_assignments = params.dig(:issue, :role_assignments)
        return unless role_assignments

        issue.issue_role_assignments.destroy_all
        build_role_assignments_for_issue(issue, role_assignments)

        all_assigned_ids = issue.issue_role_assignments
                                .map(&:assigned_user_ids)
                                .flatten
                                .uniq
        #Rails.logger.info "[Eventer] Overwriting assigned_user_ids with role-based (edit): #{all_assigned_ids.inspect}"
        issue.assigned_user_ids = all_assigned_ids
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
