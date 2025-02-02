class UsersDataController < ApplicationController
  before_action :require_admin, only: [:index, :show]

  def index
    @users_data = User.all
  end

  def show
    @user_data = User.find(params[:id])
  end

  private

  def require_admin
    unless User.current.admin?
      render_403
    end
  end
end
