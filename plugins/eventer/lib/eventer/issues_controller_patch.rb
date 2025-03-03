module Eventer
  module IssuesControllerPatch
    def self.included(base)
      base.class_eval do
        before_action :override_assignee_param, only: [:create, :update, :show]

        private

        def override_assignee_param
          if params[:issue]
            # If multiple assignees exist, override `assigned_to_id` with an array
            params[:issue][:assigned_to_id] = params[:issue][:assigned_user_ids]&.first
          end
        end
      end
    end
  end
end

Rails.configuration.to_prepare do
  unless IssuesController.included_modules.include?(Eventer::IssuesControllerPatch)
    IssuesController.send(:include, Eventer::IssuesControllerPatch)
  end
end
