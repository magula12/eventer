# plugins/eventer/app/controllers/qualifications_controller.rb
class QualificationsController < ApplicationController
  def new
    @qualification = UserRoleQualification.new
  end

  def edit
    @qualification = UserRoleQualification.find(params[:id])
  end

  def create
    ActiveRecord::Base.transaction do
      UserRole.create!(
        user_id: params[:user_id],
        role_id: params[:role_id]
      )

      UserRoleQualification.create!(
        user_id: params[:user_id],
        role_id: params[:role_id],
        category_id: params[:category_id],
        rating: params[:rating]
      )
    end

    redirect_to users_data_path(params[:user_id]), notice: I18n.t('flash.qualification_added')
  rescue ActiveRecord::RecordInvalid => e
    flash[:error] = I18n.t('flash.qualification_create_error', error: e.message)
    render :new
  end

  def destroy
    ActiveRecord::Base.transaction do
      qualification = UserRoleQualification.find(params[:id])
      user_id = qualification.user_id
      role_id = qualification.role_id

      qualification.destroy!

      if UserRoleQualification.where(user_id: user_id, role_id: role_id).none?
        UserRole.find_by(user_id: user_id, role_id: role_id)&.destroy!
      end
    end

    redirect_to users_data_path(params[:user_id]), notice: I18n.t('flash.qualification_deleted')
  rescue ActiveRecord::RecordNotFound
    flash[:error] = I18n.t('flash.qualification_not_found')
    redirect_to users_data_path(params[:user_id])
  rescue ActiveRecord::RecordInvalid => e
    flash[:error] = I18n.t('flash.qualification_delete_error', error: e.message)
    redirect_to users_data_path(params[:user_id])
  end
end