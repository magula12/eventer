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

match 'eventer_api',
      :to => 'eventer_api#index',
      :via => :get,
      :defaults => { format: 'json' }

match 'eventer_api',
      :to => 'eventer_api#create_assignments',
      :via => :post,
      :defaults => { format: 'json' }

match 'run_match_script',
      :to => 'python_runner#run_script',
      :via => :post,
      :as => :run_match_script

# Show the algorithm runner page
match "algorithm_runner",
      to: "algorithm_runner#index",
      via: :get,
      as: :algorithm_runner

# Endpoint to POST run the script
match "algorithm_runner/run",
      to: "algorithm_runner#run_script",
      via: :post,
      as: :run_script_algorithm

