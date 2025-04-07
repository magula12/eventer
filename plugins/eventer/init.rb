Rails.logger.info "Loading Eventer plugin..."
require_relative 'lib/eventer/issue_patch'
#require_relative 'lib/eventer/issues_controller_patch'
require_relative  'app/controllers/custom_filters_controller'
require_relative 'lib/eventer/hooks/multi_assignee_hook'
require_relative 'lib/eventer/hooks/view_multi_assignee_hook'

Redmine::Plugin.register :eventer do
  name 'Eventer plugin'
  author 'Tomáš Magula'
  description 'This is a plugin for Redmine'
  version '1.0.0'
  url 'http://example.com/path/to/plugin'
  author_url 'http://example.com/about'

  menu :top_menu, :offdays,
       { controller: 'offdays', action: 'index', user_id: User.current.id },
       caption: :label_offdays

  menu :top_menu, :eventer_filters,
       { controller: 'custom_filters', action: 'index' },
       caption: :label_custom_filters

  menu :admin_menu, :users_data,
       { controller: 'users_data', action: 'index' },
       caption: :label_users_data

end
Issue.include Eventer::IssuePatch