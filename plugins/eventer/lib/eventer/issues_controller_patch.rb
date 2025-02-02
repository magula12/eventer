module Eventer
  module IssuesControllerPatch
    extend ActiveSupport::Concern

    included do |othermod|
      before_action :set_assigned_users, only: [:new, :edit, :create, :update]
      Rails.logger.info "Issues controller patch start..."
    end

    def new
      @issue = Issue.new
      # Initialize with an empty array for assigned users
      @issue.assigned_users = []
    end

    def create
      @issue = Issue.new(issue_params)
      if @issue.save
        flash[:notice] = 'Issue was successfully created.'
        redirect_to issue_path(@issue)
      else
        render :new
      end
    end

    def edit
      @issue = Issue.find(params[:id])
    end

    def update
      @issue = Issue.find(params[:id])
      if @issue.update(issue_params)
        flash[:notice] = 'Issue was successfully updated.'
        redirect_to issue_path(@issue)
      else
        render :edit
      end
    end

    private

    def issue_params
      params.require(:issue).permit(:subject, :description, assigned_user_ids: [])
    end

    def set_assigned_users
      @issue.assigned_users ||= []
    end
  end
end