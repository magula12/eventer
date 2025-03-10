class CustomFiltersController < ApplicationController
  before_action :find_filter, only: [:edit, :update, :destroy]

  def index
    @filters = CustomFilter.where(user_id: User.current.id)

    if @filters.empty?
      flash[:notice] = "Nemáte žiadne filtre. Vytvorte nový!"
    end
  end


  def new
    @filter = CustomFilter.new
  end

  def create
    @filter = CustomFilter.new(filter_params)
    @filter.user = User.find(User.current.id)

    if @filter.conditions.blank?
      @filter.conditions = { "conditions" => { "and" => [] }, "rules" => { "and" => [] } } # Ensure a valid JSON structure
    end

    if @filter.save
      redirect_to custom_filters_path, notice: 'Filter bol úspešne vytvorený.'
    else
      flash.now[:alert] = 'Nepodarilo sa vytvoriť filter. Skontrolujte dáta.'
      render :new
    end
  end


  def edit; end

  def update
    if @filter.update(filter_params)
      redirect_to custom_filters_path, notice: 'Filter was successfully updated.'
    else
      render :edit
    end
  end

  def destroy
    @filter.destroy
    redirect_to custom_filters_path, notice: 'Filter was successfully deleted.'
  end

  private

  def find_filter
    @filter = CustomFilter.find(params[:id])
  end

  def filter_params
    params.require(:custom_filter).permit(:name, :conditions)
  end
end
