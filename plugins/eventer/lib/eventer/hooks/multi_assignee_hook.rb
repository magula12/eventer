module Eventer
  module Hooks
    class MultiAssigneeHook < Redmine::Hook::Listener
      def controller_issues_create_before_save(context = {})
        Rails.logger.info "[Eventer] MultiAssigneeHook (create) triggered"
        issue = context[:issue]
        params = context[:params]
        if params[:issue] && params[:issue][:assigned_user_ids]
          assigned_ids = params[:issue][:assigned_user_ids].reject(&:blank?)
          Rails.logger.info "[Eventer] Setting assigned_user_ids to: #{assigned_ids.inspect}"
          issue.assigned_user_ids = assigned_ids
        end
      end

      def controller_issues_edit_before_save(context = {})
        Rails.logger.info "[Eventer] MultiAssigneeHook (edit) triggered"
        issue = context[:issue]
        params = context[:params]
        if params[:issue] && params[:issue][:assigned_user_ids]
          assigned_ids = params[:issue][:assigned_user_ids].reject(&:blank?)
          Rails.logger.info "[Eventer] Setting assigned_user_ids to: #{assigned_ids.inspect}"
          issue.assigned_user_ids = assigned_ids
        end
      end
    end
  end
end
