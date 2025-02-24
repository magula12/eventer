class QualificationsController < ApplicationController
  def new
    @qualification = UserRoleQualification.new
  end

  def edit
    @qualification = UserRoleQualification.find(params[:id])
  end

  def create
    ActiveRecord::Base.transaction do
      # Create UserRole
      UserRole.create!(
        user_id: params[:user_id],
        role_id: params[:role_id]
      )

      # Create UserRoleQualification
      UserRoleQualification.create!(
        user_id: params[:user_id],
        role_id: params[:role_id],
        category_id: params[:category_id],
        rating: params[:rating]
      )
    end

    redirect_to users_data_path(params[:user_id]), notice: "Kvalifikácia bola úspešne pridaná."
  rescue ActiveRecord::RecordInvalid => e
    flash[:error] = "Chyba: #{e.message}"
    render :new
  end

  def destroy
    ActiveRecord::Base.transaction do
      qualification = UserRoleQualification.find(params[:id])
      user_id = qualification.user_id
      role_id = qualification.role_id

      # Delete UserRoleQualification
      qualification.destroy!

      # Delete UserRole if no more qualifications exist for this user and role
      if UserRoleQualification.where(user_id: user_id, role_id: role_id).none?
        UserRole.find_by(user_id: user_id, role_id: role_id)&.destroy!
      end
    end

    redirect_to users_data_path(params[:user_id]), notice: "Kvalifikácia bola úspešne odstránená."
  rescue ActiveRecord::RecordNotFound
    flash[:error] = "Chyba: Kvalifikácia neexistuje."
    redirect_to users_data_path(params[:user_id])
  rescue ActiveRecord::RecordInvalid => e
    flash[:error] = "Chyba pri odstraňovaní: #{e.message}"
    redirect_to users_data_path(params[:user_id])
  end

end
