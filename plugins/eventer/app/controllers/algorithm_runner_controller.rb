# plugins/eventer/app/controllers/algorithm_runner_controller.rb
class AlgorithmRunnerController < ApplicationController
  before_action :require_admin  # optional: restrict to admin

  # GET /algorithm_runner
  def index
    # Just render the page with the button
  end

  # POST /algorithm_runner/run
  def run_script
    # We'll run the Python script via system call
    script_dir  = "/usr/src/redmine/plugins/eventer/python"
    script_path = File.join(script_dir, "main.py")
    python_path = File.join(script_dir, "venv", "bin", "python")

    command = "cd #{script_dir} && #{python_path} #{script_path} 2>&1"
    Rails.logger.info "RUN_SCRIPT: Executing => #{command.inspect}"

    @output = `#{command}`    # capture stdout/stderr
    @status = $?.exitstatus   # get the exit code

    Rails.logger.info "RUN_SCRIPT: Output => #{@output}"
    Rails.logger.info "RUN_SCRIPT: Exit code => #{@status}"

    # We'll stay on the same page, so let's store the data in instance vars
    if @status == 0
      flash.now[:notice] = "Python script ran successfully!"
    else
      flash.now[:error] = "Python script failed with code #{@status}"
    end

    # We'll re-render `index.html.erb` to show the output
    render :index
  end
end
