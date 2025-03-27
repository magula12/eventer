# plugins/eventer/app/controllers/algorithm_runner_controller.rb
require 'net/http'
require 'uri'
require 'json'

class AlgorithmRunnerController < ApplicationController
  before_action :require_admin

  def index
    # Just renders the page with the button
  end

  # POST /algorithm_runner/run
  def run_script
    uri = URI.parse("http://python-service:5000/run_algorithm")
    http = Net::HTTP.new(uri.host, uri.port)
    request = Net::HTTP::Post.new(uri.path, { "Content-Type" => "application/json" })
  
    response = http.request(request)
    @status_code = response.code.to_i
  
    if @status_code == 200
      begin
        json = JSON.parse(response.body)
        @output = json["output"]
    
        # 🟢 Check if assignments were posted (based on known response)
        if @output.include?("Assignments posted successfully")
          flash.now[:notice] = "✅ Solutions from the algorithm were successfully saved into Redmine."
        else
          flash.now[:notice] = "✅ Python script ran successfully!"
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
end
