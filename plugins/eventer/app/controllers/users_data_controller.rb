# plugins/eventer/app/controllers/users_data_controller.rb
class UsersDataController < ApplicationController
  before_action :set_user, only: [:show, :new_qualification, :create_qualification, :edit_qualification, :update_qualification]

  def index
    @users_data = User.all
  end

  def show
    @user_data = @user
    @qualifications = fetch_qualities(@user_data)
  end

  def new_qualification
    @qualification = UserRoleQualification.new
  end

  def create_qualification
    @qualification = UserRoleQualification.new(qualification_params)
    @qualification.user = @user

    if @qualification.save
      redirect_to users_data_path(@user), notice: I18n.t('flash.qualification_added')
    else
      render :new_qualification
    end
  end

  def edit_qualification
    @qualification = UserRoleQualification.find(params[:id])
  end

  def update_qualification
    @qualification = UserRoleQualification.find(params[:id])

    if @qualification.update(qualification_params)
      redirect_to users_data_path(@user), notice: I18n.t('flash.qualification_updated')
    else
      render :edit_qualification
    end
  end

  private

  def set_user
    @user = User.find(params[:id])
  end

  def fetch_qualities(user)
    UserRoleQualification
      .where(user_id: user.id)
      .includes(:role, :category)
      .map do |qualification|
      {
        id: qualification.id,
        role_name: qualification.role&.name || 'Unknown Role',
        category_name: qualification.category&.name || 'Unknown Category',
        role_id: qualification.role_id,
        rating: qualification.rating
      }
    end
  rescue => e
    Rails.logger.error "Error fetching qualities: #{e.message}"
    []
  end

  def qualification_params
    params.require(:user_role_qualification).permit(:role_id, :category_id, :rating)
  end
end