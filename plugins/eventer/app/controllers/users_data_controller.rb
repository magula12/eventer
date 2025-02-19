class UsersDataController < ApplicationController
  before_action :set_user, only: [:show]

  def index
    @users_data = User.all
  end

  def show
    @user_data = User.find_by(id: params[:id]) # Use find_by to avoid exceptions
    unless @user_data
      Rails.logger.error "User with ID #{params[:id]} not found"
      redirect_to users_data_path, alert: "User not found" and return
    end

    @qualities = fetch_qualities(@user_data)
  end

  private

  def set_user
    @user = User.find(params[:id])
  end

  def fetch_qualities(user)
    UserRoleQualification
      .where(user_id: user.id)
      .includes(:role, :category) # Použiť správny názov asociácie
      .map do |qualification|
      {
        role_name: qualification.role&.name || 'Unknown Role',
        category_name: qualification.category&.name || 'Unknown Category', # Opravený názov
        rating: fetch_rating(user.id, qualification.role_id)
      }
    end
  rescue => e
    Rails.logger.error "Error fetching qualities: #{e.message}"
    []
  end


  def fetch_rating(user_id, role_id)
    UserRole.find_by(user_id: user_id, role_id: role_id)&.rating || 'No Rating'
  end
end
