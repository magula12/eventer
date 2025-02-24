module Eventer
  module IssuesControllerPatch
    def self.included(base)
      base.class_eval do
        alias_method :issue_params_without_multi, :issue_params
        def issue_params
          permitted = issue_params_without_multi
          if params[:issue] && params[:issue][:assigned_user_ids]
            # Ensure the parameter is an array
            permitted[:assigned_user_ids] = params[:issue][:assigned_user_ids].reject(&:blank?)
          end
          permitted
        end
      end
    end
  end

  #IssuesController.send(:include, IssuesControllerPatch)
end