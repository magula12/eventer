# plugins/eventer/app/controllers/eventer_api_controller.rb
class EventerApiController < ApplicationController
  accept_api_auth :index  # Allows API authentication via key

  def index
    # Fetch issues with required roles
    issues = Issue.includes(:issue_role_assignments, :category).limit(10).map do |issue|
      {
        id: issue.id,
        subject: issue.subject,
        start_datetime: issue.start_date,
        end_datetime: issue.due_date,
        category: issue.category&.name,
        category_priority: issue.category&.priority,
        priority: issue.priority&.name,

        # Required roles for this issue
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

    # Fetch users including qualifications, off days, and custom filters
    users = User.includes(:user_role_qualifications, :off_days, :custom_filters).limit(10).map do |user|
      {
        id: user.id,
        login: user.login,
        firstname: user.firstname,
        lastname: user.lastname,

        # Include qualifications
        qualifications: user.user_role_qualifications.map do |qualification|
          {
            role: qualification.role.name,
            category: qualification.category&.name,
            rating: qualification.rating
          }
        end,

        # Include only off days where end_datetime is in the future
        off_days: user.off_days.where("end_datetime > ?", Time.now).map do |off_day|
          {
            start_datetime: off_day.start_datetime,
            end_datetime: off_day.end_datetime
          }
        end,

        # Include custom filters without modifying JSON (directly return stored conditions)
        custom_filters: user.custom_filters.map do |filter|
          {
            name: filter.name,
            conditions: filter.conditions # Directly return the stored JSON
          }
        end
      }
    end

    render json: {
      issues: issues,
      users: users
    }
  end
end
