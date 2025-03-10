# plugins/eventer/lib/eventer/user_patch.rb
module Eventer
  module UserPatch
    extend ActiveSupport::Concern

    included do
        has_many :user_role_qualifications, foreign_key: 'user_id'
        has_many :off_days, foreign_key: 'user_id'
        has_many :custom_filters, foreign_key: 'user_id'
      end
    end
  end

unless User.included_modules.include?(Eventer::UserPatch)
  User.send(:include, Eventer::UserPatch)
end