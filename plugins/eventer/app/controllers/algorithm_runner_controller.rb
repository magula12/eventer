# plugins/eventer/app/controllers/algorithm_runner_controller.rb
require 'net/http'
require 'uri'
require 'json'
require 'date'

class AlgorithmRunnerController < ApplicationController
  before_action :require_admin

  def index
    # Just renders the page with the button
  end

  # POST /algorithm_runner/run
  def run_script
    start_date = params[:start_date].presence && DateTime.parse(params[:start_date])
    end_date = params[:end_date].presence && DateTime.parse(params[:end_date])

    # Fetch all issues and users
    all_data = fetch_json_from_api
    if all_data.nil?
      flash.now[:error] = "❌ Failed to fetch data from API."
      render :index and return
    end

    filtered_issues = all_data["issues"]
    users = all_data["users"]

    if start_date && end_date
      filtered_issues = filtered_issues.select do |issue|
        issue_start = DateTime.parse(issue["start_datetime"]) rescue nil
        issue_end = DateTime.parse(issue["end_datetime"]) rescue nil
        next false unless issue_start && issue_end
        issue_start >= start_date && issue_end <= end_date
      end
    end

    payload = {
      issues: filtered_issues,
      users: users,
      partial_solution: params[:partial_solution] == '1'
    }

    uri = URI.parse("http://python-service:5000/run_algorithm")
    http = Net::HTTP.new(uri.host, uri.port)
    request = Net::HTTP::Post.new(uri.path, { "Content-Type" => "application/json" })
    request.body = payload.to_json

    response = http.request(request)
    @status_code = response.code.to_i

    if @status_code == 200
      begin
        json = JSON.parse(response.body)
        @output = json["output"]

        if @output.include?("ILP did not reach an optimal solution")
          flash.now[:warning] = "Infeasible solution found."
          else
            if @output.include?("Assignments posted successfully!")
              flash.now[:notice] = "✅ Python script ran successfully!"
            end
        end

      rescue => e
        @output = "✅ Algorithm ran, but response could not be parsed:\n#{response.body}"
        flash.now[:warning] = "⚠️ Output parsing failed: #{e.message}"
      end
    else
      @output = "❌ Algorithm failed (HTTP #{@status_code}).\n\n#{response.body}"
      flash.now[:error] = "❌ Python service returned an error (#{@status_code})"
    end

    render :index
  end

  private

  def fetch_json_from_api
    uri = URI.parse("http://redmine:3000/eventer_api.json?key=836415703b4576d4dc5663a062a89b3a7b10055f")
    response = Net::HTTP.get_response(uri)
    return nil unless response.is_a?(Net::HTTPSuccess)
    JSON.parse(response.body)
  rescue => e
    Rails.logger.error("Error fetching API data: #{e.message}")
    nil
  end
end
