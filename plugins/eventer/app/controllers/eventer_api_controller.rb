# plugins/eventer/app/controllers/eventer_api_controller.rb
class EventerApiController < ApplicationController
  accept_api_auth :index, :create_assignments

  # POST to /eventer_api.json
  def index
    # existing code for fetching data
    issues = Issue.includes(:issue_role_assignments, :category).limit(10).map do |issue|
      {
        id: issue.id,
        subject: issue.subject,
        start_datetime: issue.start_datetime,
        end_datetime: issue.end_datetime,
        category: issue.category&.name,
        category_priority: issue.category&.priority,
        priority: issue.priority&.name,
        required_roles: issue.issue_role_assignments.map do |assignment|
          {
            role: assignment.role.name,
            required_count: assignment.required_count,
            assigned_users: User.where(id: assignment.assigned_user_ids).map do |user|
              {
                id: user.id,
                firstname: user.firstname,
                lastname: user.lastname
              }
            end
          }
        end
      }
    end

    users = User.includes(:user_role_qualifications, :off_days, :custom_filters).limit(10).map do |user|
      {
        id: user.id,
        login: user.login,
        firstname: user.firstname,
        lastname: user.lastname,
        qualifications: user.user_role_qualifications.map do |qualification|
          {
            role: qualification.role.name,
            category: qualification.category&.name,
            rating: qualification.rating
          }
        end,
        off_days: user.off_days.where("end_datetime > ?", Time.now).map do |off_day|
          {
            start_datetime: off_day.start_datetime,
            end_datetime: off_day.end_datetime
          }
        end,
        custom_filters: user.custom_filters.map do |filter|
          {
            name: filter.name,
            conditions: filter.conditions
          }
        end
      }
    end

    render json: { issues: issues, users: users }
  end

  # POST from /eventer_api.json
  def create_assignments
    Rails.logger.info "CREATE_ASSIGNMENTS: Start processing POST data."

    # Convert to a real Hash
    # to_unsafe_h allows all keys without strong_parameters whitelisting
    assignments = params[:assignments].to_unsafe_h

    unless assignments.is_a?(Hash)
      Rails.logger.info "CREATE_ASSIGNMENTS: 'assignments' is missing or not a Hash. Current params: #{params.inspect}"
      render json: { error: "Missing or invalid 'assignments' payload" }, status: :bad_request
      return
    end

    Rails.logger.info "CREATE_ASSIGNMENTS: Received assignments => #{assignments.inspect}"

    assignments.each do |issue_id_str, roles|
      issue_id = issue_id_str.to_i
      issue = Issue.find_by(id: issue_id)
      next unless issue

      roles.each do |role_name, user_ids|
        role = Role.find_by(name: role_name)
        next unless role

        assignment = issue.issue_role_assignments.find_by(role_id: role.id)
        next unless assignment

        assignment.assigned_user_ids = user_ids.map(&:to_s)
        assignment.save
        Rails.logger.info "CREATE_ASSIGNMENTS: Updated issue=#{issue_id}, role='#{role_name}' => #{user_ids.inspect}"
      end
    end

    render json: { status: "Assignments updated" }, status: :ok
  end

end
