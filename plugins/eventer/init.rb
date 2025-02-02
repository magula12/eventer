Rails.logger.info "Loading Eventer plugin..."

require_relative 'lib/eventer/issue_patch'
require_relative 'lib/eventer/issues_controller_patch'
require_relative 'lib/eventer/users_controller_patch'
require_relative  'app/controllers/custom_filters_controller'



Redmine::Plugin.register :eventer do
  name 'Eventer plugin'
  author 'Author name'
  description 'This is a plugin for Redmine'
  version '0.0.1'
  url 'http://example.com/path/to/plugin'
  author_url 'http://example.com/about'


  Rails.application.config.assets.precompile += %w[offdays.css]

  menu :top_menu, :offdays, { controller: 'offdays', action: 'index', user_id: User.current.id }, caption: 'Offdays'
  menu :top_menu, :eventer_filters, { controller: 'custom_filters', action: 'index' }, caption: 'Filters'
  menu :admin_menu, :users_data, { controller: 'users_data', action: 'index' }, caption: 'Users Data'


end

#Rails.logger.info "Including Eventer::IssuePatch in Issue model..."
IssuesController.send(:include, Eventer::IssuesControllerPatch)
Issue.include Eventer::IssuePatch
UsersController.include Eventer::UsersControllerPatch