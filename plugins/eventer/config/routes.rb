# Plugin's routes
# See: http://guides.rubyonrails.org/routing.html

# resources :users do
#   resources :offdays, only: [:index]
# end
resources :users_data, only: [:index, :show]

resources :qualifications, only: [:new, :create, :edit, :update, :destroy]

resources :offdays, only: [:index, :create, :destroy]

RedmineApp::Application.routes.draw do
  scope '/eventer' do
    resources :custom_filters
  end
end

