class OffdaysController < ApplicationController
  def index
    if current_user.is_a?(AnonymousUser)
      Rails.logger.info "Anonymous user accessed off days at #{Time.now}"
      @off_days = [] # Return an empty array for anonymous users
    else
      @off_days = fetch_off_days_for_user(current_user.id)
    end
  end

  def current_user
    # Assuming you have a method to get the current user
    User.find(session[:user_id]) rescue AnonymousUser.new
  end

  def fetch_off_days_for_user(user_id)
    # Query the database for the user's off days
    OffDay.where(user_id: user_id)
  end

    def create
      @off_day = OffDay.new(off_day_params)
      @off_day.user_id = current_user.id

      if @off_day.save
        flash[:notice] = 'Off day added successfully!'
        redirect_to offdays_path
      else
        flash[:error] = 'Failed to add off day.'
        render :index
      end
    end

    def destroy
      @off_day = OffDay.find_by(id: params[:id], user_id: current_user.id)

      if @off_day&.destroy
        flash[:notice] = 'Off day deleted successfully!'
      else
        flash[:error] = 'Failed to delete off day.'
      end

      redirect_to offdays_path
    end

    private

    def off_day_params
      params.require(:off_day).permit(:start_datetime, :end_datetime)
    end
end