#not applied

module Eventer
  module UsersControllerPatch
    extend ActiveSupport::Concern

    included do
      Rails.logger.info "Users controller patch start..."
      # This hook will ensure the patch is applied only to the show action
      #before_action :add_qualities_to_user, only: [:show]

      # Alias original `show` method to preserve its functionality
      alias_method :show_without_qualities, :show

    def show
      Rails.logger.debug "Entering show_with_qualities action"

      @user = User.find(params[:id])
      @qualities = fetch_qualities(@user)

      Rails.logger.debug "Fetched qualities: #{@qualities.inspect}"

      # Call the original show action logic
      show_without_qualities
    end

    private

    def fetch_qualities(user)
      Rails.logger.debug "Fetching qualities for user: #{user.id}"

      qualifications = UserRoleQualification
                         .where(user_id: user.id)
                         .includes(:role, :issue_category)
                         .map do |qualification|
        Rails.logger.debug "Qualification: #{qualification.inspect}"
        {
          role_name: qualification.role&.name || 'Unknown Role',
          category_name: qualification.issue_category&.name || 'Unknown Category',
          rating: fetch_rating(user.id, qualification.role_id)
        }
      end
      Rails.logger.debug "Fetched qualifications: #{qualifications.inspect}"
      qualifications
    rescue => e
      Rails.logger.error "Error fetching qualities: #{e.message}"
      []
    end

    def fetch_rating(user_id, role_id)
      UserRole.find_by(user_id: user_id, role_id: role_id)&.rating || 'No Rating'
    end
    end
    end
end
