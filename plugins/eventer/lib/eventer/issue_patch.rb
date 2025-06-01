# plugins/eventer/lib/eventer/issue_patch.rb
#TODO: Tidy up this file, remove unnecessary comments, and ensure it works as expected
module Eventer
  module IssuePatch
    extend ActiveSupport::Concern

    included do
      begin
        has_many :issue_role_assignments, dependent: :destroy
        belongs_to :category, class_name: 'IssueCategory', foreign_key: 'category_id', optional: true
        belongs_to :priority, class_name: 'IssuePriority', foreign_key: 'priority_id', optional: true
        accepts_nested_attributes_for :issue_role_assignments, allow_destroy: true

        safe_attributes 'start_datetime', 'end_datetime', 'issue_role_assignments_attributes'

        validates :start_datetime, presence: true

        # Helper to get all assigned user IDs
        def assigned_user_ids
          issue_role_assignments.pluck(:assigned_user_ids).flatten.uniq.map(&:to_i).reject(&:zero?)
        end
        def assigned_user_ids=(user_ids)
          #Rails.logger.info "Was called mate! #{user_ids.inspect}"
        end

        # Override assigned_to to maintain compatibility
        def assigned_to
          User.find_by(id: assigned_user_ids.first) # Redmine expects a single user
        end

        def assigned_to=(user)
          user_ids = if user.is_a?(User)
                       [user.id]
                     else
                       Array(user).map(&:to_i).reject(&:zero?)
                     end
          role = Role.first || Role.create(name: 'Default', position: 1)
          issue_role_assignments.destroy_all
          issue_role_assignments.create(role_id: role.id, required_count: 1, assigned_user_ids: user_ids)
          #Rails.logger.info "Set assigned_user_ids for issue #{id || 'new'}: #{user_ids.join(', ')}"
        end

        # Override the assigned_to scope
        singleton_class.class_eval do
          def assigned_to(arg)
            #Rails.logger.info "Entering assigned_to scope with arg: #{arg.inspect}"
            arg = Array(arg).uniq
            ids = arg.map { |p| p.is_a?(Principal) ? p.id : p }
            ids += arg.select { |p| p.is_a?(User) }.map(&:group_ids).flatten.uniq
            ids.compact!
            if ids.any?
              where("assigned_to_id IN (:ids) OR EXISTS (SELECT 1 FROM issue_role_assignments WHERE issue_id = issues.id AND :id::text = ANY(assigned_user_ids))", id: ids, ids: ids)
            else
              none
            end
          end
        end

        # Override load_visible_relations
        def self.load_visible_relations(issues)
          return unless issues.any?

          issue_ids = issues.map(&:id)
          #Rails.logger.info "Loading visible relations for issue IDs: #{issue_ids.join(', ')}"
          begin
            relations = IssueRelation.where("issue_from_id IN (:ids) OR issue_to_id IN (:ids)", ids: issue_ids)
            relations = relations.select do |relation|
              from_issue = Issue.find_by(id: relation.issue_from_id)
              to_issue = Issue.find_by(id: relation.issue_to_id)
              user = User.current
              (from_issue && (from_issue.author_id == user.id || from_issue.assigned_to_id == user.id || from_issue.assigned_user_ids.include?(user.id))) ||
                (to_issue && (to_issue.author_id == user.id || to_issue.assigned_to_id == user.id || to_issue.assigned_user_ids.include?(user.id)))
            end
            relations.each do |relation|
              issues.detect { |issue| issue.id == relation.issue_from_id }&.relations << relation
              issues.detect { |issue| issue.id == relation.issue_to_id }&.relations << relation
            end
            #Rails.logger.info "Loaded #{relations.size} visible relations"
          rescue ActiveRecord::StatementInvalid => e
            Rails.logger.error "Error loading visible relations: #{e.message}"
          end
        end

        # Override visible_condition
        def self.visible_condition(user, options={})
          #Rails.logger.info "Entering custom visible_condition for user #{user&.id || 'anonymous'}"
          begin
            Project.allowed_to_condition(user, :view_issues, options) do |role, user|
              sql =
                if user&.id && user.logged?
                  case role&.issues_visibility
                  when 'all'
                    '1=1'
                  when 'default'
                    user_ids = [user.id] + user.groups.pluck(:id).compact
                    "(#{table_name}.is_private = #{connection.quoted_false} " \
                      "OR #{table_name}.author_id = #{user.id} " \
                      "OR #{table_name}.assigned_to_id IN (#{user_ids.join(',')}) " \
                      "OR EXISTS (SELECT 1 FROM issue_role_assignments WHERE issue_id = #{table_name}.id AND #{user.id}::text = ANY(assigned_user_ids)))"
                  when 'own'
                    user_ids = [user.id] + user.groups.pluck(:id).compact
                    "(#{table_name}.author_id = #{user.id} OR " \
                      "#{table_name}.assigned_to_id IN (#{user_ids.join(',')}) OR " \
                      "EXISTS (SELECT 1 FROM issue_role_assignments WHERE issue_id = #{table_name}.id AND #{user.id}::text = ANY(assigned_user_ids)))"
                  else
                    '1=0'
                  end
                else
                  "(#{table_name}.is_private = #{connection.quoted_false})"
                end
              unless role&.permissions_all_trackers?(:view_issues)
                tracker_ids = role&.permissions_tracker_ids(:view_issues) || []
                if tracker_ids.any?
                  sql = "(#{sql} AND #{table_name}.tracker_id IN (#{tracker_ids.join(',')}))"
                else
                  sql = '1=0'
                end
              end
              #Rails.logger.info "Generated visible_condition SQL for user #{user&.id || 'anonymous'}: #{sql}"
              sql
            end
          rescue ActiveRecord::StatementInvalid => e
            Rails.logger.error "Error in visible_condition: #{e.message}"
            '1=0'
          end
        end
      rescue StandardError => e
        Rails.logger.error "Failed to set up issue patch: #{e.message}"
      end
    end
  end
end

unless Issue.included_modules.include?(Eventer::IssuePatch)
  Issue.send(:include, Eventer::IssuePatch)
  Rails.logger.info 'Eventer::IssuePatch included'
end
