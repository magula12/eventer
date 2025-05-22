module Eventer
  module IssuesControllerPatch
    def self.included(base)
      base.class_eval do
        skip_before_action :find_issue, only: :show
        skip_before_action :authorize, only: :show
        before_action :handle_issue_role_assignments, only: [:create, :update]
        before_action :custom_find_issue, only: :show

        private

        def handle_issue_role_assignments
          Rails.logger.info "Processing issue params: #{params[:issue]&.inspect}"
          if params[:issue] && params[:issue][:issue_role_assignments_attributes]
            params[:issue][:issue_role_assignments_attributes].each do |_, attrs|
              if attrs[:assigned_user_ids]
                attrs[:assigned_user_ids] = attrs[:assigned_user_ids].reject(&:blank?).map(&:to_i).uniq
                Rails.logger.info "Received assigned_user_ids for role #{attrs[:role_id]}: #{attrs[:assigned_user_ids].join(', ')}"
              else
                attrs[:assigned_user_ids] = []
              end
              attrs[:required_count] = attrs[:required_count].to_i if attrs[:required_count]
            end
            first_assignment = params[:issue][:issue_role_assignments_attributes].values.find { |a| a[:assigned_user_ids].any? }
            params[:issue][:assigned_to_id] = first_assignment[:assigned_user_ids].first if first_assignment
          else
            Rails.logger.info "No issue_role_assignments_attributes in params: #{params[:issue]&.inspect}"
            params[:issue][:issue_role_assignments_attributes] = []
          end
        end

        def custom_find_issue
          Rails.logger.info "Patch loaded and custom_find_issue running"
          Rails.logger.info "Custom find_issue for user #{User.current.id}, issue #{params[:id]}"
          begin
            issue = Issue.find_by(id: params[:id].to_i)
            if issue
              Rails.logger.info "Issue #{params[:id]}: author_id=#{issue.author_id}, assigned_to_id=#{issue.assigned_to_id}, is_private=#{issue.is_private}, project_id=#{issue.project_id}, assigned_user_ids=#{issue.issue_role_assignments.map { |a| a.assigned_user_ids }.inspect}"
              project = issue.project
              roles = User.current.roles_for_project(project)
              visibility = roles.map(&:issues_visibility).uniq
              Rails.logger.info "User #{User.current.id} visibility: #{visibility.inspect}"

              allow_access = false
              if visibility.include?('all')
                allow_access = true
              elsif visibility.include?('own')
                allow_access = issue.author_id == User.current.id ||
                  issue.assigned_to_id == User.current.id ||
                  issue.issue_role_assignments.any? { |a| a.assigned_user_ids.include?(User.current.id) }
              end

              if allow_access
                @issue = issue
                @project = project
                Rails.logger.info "User #{User.current.id} authorized for issue #{params[:id]}"
              else
                Rails.logger.warn "User #{User.current.id} not authorized for issue #{params[:id]}"
                render_403
                return false
              end

              unless User.current.allowed_to?(:view_issues, @project)
                Rails.logger.warn "User #{User.current.id} lacks :view_issues permission for project #{@project.id}"
                render_403
                return false
              end
            else
              Rails.logger.warn "Issue #{params[:id]} does not exist"
              render_404
              return false
            end
            Rails.logger.info "Issue #{params[:id]} found for user #{User.current.id}"
          rescue ActiveRecord::RecordNotFound
            Rails.logger.warn "Issue #{params[:id]} not found"
            render_404
            return false
          rescue StandardError => e
            Rails.logger.error "Error in custom_find_issue for issue #{params[:id]}: #{e.message}"
            render_403
            return false
          end
        end
      end
    end
  end
end

unless IssuesController.included_modules.include?(Eventer::IssuesControllerPatch)
  IssuesController.send(:include, Eventer::IssuesControllerPatch)
  Rails.logger.info 'Eventer::IssuesControllerPatch included'
end