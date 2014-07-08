def check_required_variables
    missing_vars = 0
    # Check for required variables before running a task
    vars = [
        # Address of the remote server to ssh / scp files to
        "$remote",
        # Port of the remote server to ssh into
        "$remote_port",
        # Directory on the remote for the app
        "$root",
        # Filename of the app's primary file to run
        "$script_name",
        # Name and description of what the app does
        "$app_name",
        # The user that should run the app (ownership of files)
        "$user",
        # Commands that must exist (be installed) on the remote server before
        # this app can run. Default value: []
        "$required_commands",
        # Pattern of files and directories that should be uploaded to the
        # remote server every time the app is updated
        "$app_files_to_copy",
        # Pattern of files and directories to specifically exclude when
        # copying app files to the server
        "$app_files_to_exclude",

        # --- Node specific variables ---
        # Path and flags of the nodejs binary to run
        "$node_binary",
    ].each { |var_name|
        begin
            var = eval(var_name)
        rescue Exception => e
            puts "Add variable #{var_name} to the project Rakefile."
            missing_vars += 1
        end
    }
    if missing_vars > 0
        puts "ERROR: #{missing_vars} missing variable#{if missing_vars > 1 then 's' end} not found in the project Rakefile."
        exit 1
    end
end

# Check for required variables, and set up a background SSH master process
check_required_variables()
$ssh_master_file = ".ssh-master_%r_%h_%p"
# SSH flags being used:
# -f: background the SSH session
# -M : place the SSH client into master mode for connection sharing
# -N : do not execute a remote command
# -S : specifies the location of a control socket for connection sharing
# -o ControlPersist=n : timeout in seconds to kill the master ssh session if inactive
# -p : remote port to connect to via ssh
system("ssh -fMN -S #{$ssh_master_file} -o ControlPersist=10 -p #{$remote_port} #{$remote}")

desc 'Initialize the app'
task :init do
    Rake::Task[:check_required_tools].invoke
    Rake::Task[:update_app].invoke
    Rake::Task[:update_requirements].invoke
    Rake::Task[:update_nginx].invoke
end

desc 'Check for required tools'
task :check_required_tools do
    # Tools specific to this Rakefile that *must* be included
    $required_commands ||= [] # create empty array if the variable isn't defined
    $required_commands | ['nginx', 'npm', 'nodejs'] # union these arrays

    # Check for tools and missing commands
    puts "Checking for required tools..."
    missing_commands = 0
    $required_commands.each do |cmd|
        if not is_installed?(cmd)
            puts "#{cmd} not installed on server"
            missing_commands += 1
        else
            puts "#{cmd} found"
        end
    end
    if missing_commands > 0
        puts "ERROR: #{missing_commands} required tool#{if missing_commands > 1 then 's' end} missing."
        exit 1
    end
    puts "All required tools installed."
end

desc 'Update the nginx configuration'
task :update_nginx do
    dest = "#{$remote}:#{$root}"
    nginx_conf = "nginx.conf"
    scp(nginx_conf, dest)
    ssh('sudo service nginx restart', interactive: true)
end

desc 'Update the app'
task :update_app do
    dest = "#{$remote}:#{$root}app"
    $app_files_to_copy.each {|f| scp(f, dest)}
end

desc 'Restart the app'
task :restart_app do
    dest = "#{$remote}:#{$root}app"
    # Check to make sure we have all the required files on the server
    missing_required_files = 0
    $required_files.each do |f|
        # SSH flags being used:
        # -S : specifies the location of a control socket for connection sharing
        # -p : remote port to connect to via ssh
        output = `ssh -S #{$ssh_master_file} -p #{$remote_port} #{$remote} 'ls #{$root}#{f}'`
        if output.chomp != $root+f
            puts "Required file missing on server: #{f}"
            missing_required_files += 1
        end
    end
    if missing_required_files > 0
        puts "ERROR: #{missing_required_files} required file#{if missing_required_files > 1 then 's' end} missing on server."
        exit 1
    end

    # An active process should include the full path to the script (to avoid two processes running with the same script base filename)
    app = $root+'app/'+$script_name

    # Kill the active application processes
    puts "Killing existing #{$app_name} server processes:"
    ssh("ps auxww | grep \"#{app}\" | grep -v \"grep\" | awk \"{print \\$2}\" | xargs --no-run-if-empty kill")
    # Start the app
    puts "Starting #{$app_name} in the background:"
    # TODO: In the future, this should be replaced with nvm + handling of
    # specific versions of node / enabling Harmony support. For now, we leave
    # finding the right binary to the project Rakefile via $node_binary
    ssh("cd #{$root}; sh -c \"nohup #{node_binary} #{app} > nohup.out 2>&1 &\"")
    puts "Restarted the #{$app_name} application."
end

desc 'Tails the application log'
task :tail_log do
    puts "Tailing nohup.out for the #{$app_name} process:"
    ssh("cd #{$root}; tail -f nohup.out")
end

desc 'Update external Node.js dependencies on the remote host'
task :update_requirements do
    puts 'Updating packages from package.json on remote host:'
    cmd = "cd #{$root}app; npm install"
    ssh(cmd)
end

# Copy a file to the specificed remote directory
def scp(local_file, remote_dir)
    excluded = $app_files_to_exclude.map {|f| '--exclude=' + f}.join(' ')
    # SSH flags being used:
    # -S : specifies the location of a control socket for connection sharing
    # -p : remote port to connect to via ssh
    # ---
    # rsync flags being used:
    # -e : specify an alternate remote shell program (specific ssh flags)
    # -r : copy directories recursively
    # -p : set destination permission to be the same as source premissions
    # -v : verbose mode
    # -z : compress data
    sh "rsync -e 'ssh -S #{$ssh_master_file} -p #{$remote_port}' -rpvz #{excluded} #{local_file} #{$user}@#{remote_dir}/"
end

# Run an arbitrary command via SSH
def ssh(command, interactive: false, quiet: false, quiet_ssh: true)
    # Use the background ssh master process and ssh in, using interactive mode based on flags passed
    # SSH flags being used:
    # -S : specifies the location of a control socket for connection sharing
    # -t : force pseudo-tty allocation (allow interactive sessions for things like entering passwords)
    # -p : remote port to connect to via ssh
    ssh_cmd = "ssh -S #{$ssh_master_file} #{interactive ? '-t' : ''} -p #{$remote_port} #{$remote} '#{command}'#{interactive ? '' : '; echo $?'}"
    unless quiet then puts command end
    unless quiet_ssh then puts ssh_cmd end
    if interactive
        system(ssh_cmd)
    else
        exit_code = `#{ssh_cmd}`
        return exit_code
    end
end

def is_installed?(cmd)
    out = ssh("which #{cmd} >/dev/null 2>&1 && exit 0 || exit 1", quiet: true)
    if not out.chomp == '0' then return false end
    return true
end
