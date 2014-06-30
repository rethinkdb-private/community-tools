$required_commands = ['nginx', 'npm', 'nodejs']

desc 'Initialize the app'
task :init do
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
        fail "ERROR: #{missing_commands} required tool#{if missing_commands > 1 then 's' end} missing."
    end
    puts "All required tools installed."
    $directories_required.each{|d| ssh("mkdir -p #{$root}#{d}")}
    Rake::Task[:update_app].invoke
    Rake::Task[:update_requirements].invoke
    Rake::Task[:update_nginx].invoke
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
    $required_files.each do |f|
        output = `ssh #{$remote} -p 440 'ls #{$root}#{f}'`
        if output.chomp != $root+f
            fail "Required file missing on server: #{f}"
        end
    end
    app = $root+'app/'+$script_name
    # Kill the active application processes
    puts "Killing existing #{$app_name} server processes:"
    ssh("ps auxww | grep \"#{app}\" | grep -v \"grep\" | awk \"{print \\$2}\" | xargs --no-run-if-empty kill")
    # Start the app
    puts "Starting #{$app_name} in the background:"
    ssh("cd #{$root}; sh -c \"nohup nodejs #{app} > nohup.out 2>&1 &\"")
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
    sh "rsync -e 'ssh -p 440' -rpvz #{excluded} #{local_file} #{$user}@#{remote_dir}"
end

# Run an arbitrary command via SSH
def ssh(command, interactive: false, quiet: false, quiet_ssh: true)
    ssh_cmd = "ssh #{$remote} #{interactive ? '-t' : ''} -p 440 '#{command}'#{interactive ? '' : '; echo $?'}"
    unless quiet then puts command end
    unless quiet_ssh then puts ssh_cmd end
    if interactive
        sh "ssh #{$remote} -t -p 440 '#{command}'"
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
