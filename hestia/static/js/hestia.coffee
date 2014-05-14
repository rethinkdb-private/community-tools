# See documentation on the DYMO format in /docs
window.hestia = {
    debug : false,
    css_transition_duration: 100,
}

$ ->
    if not dymo? or not dymo.label? or not dymo.label.framework?
        console.log "DYMO JS framework not loaded, make sure the DYMO JS library is available."
    else
        hestia.d = dymo.label.framework
    dymo_framework_check()
    $('#submit').on 'click', (event) ->
        event.preventDefault()
    $('.reload-page').on 'click', (event) ->
        event.preventDefault()
        location.reload()
    $('input#github-username').on 'blur', (event) ->
        name = $('input#github-username').val()
        if name.length > 0 then find_github_user(name)


###
# -------------------
# DYMO labeling magic
# -------------------
###

# Check if our environment is ready (e.g. the DYMO library is available and ready)
dymo_framework_check = ->
    env = hestia.d.checkEnvironment()
    if hestia.debug then console.log 'DYMO environment: ', env
    if not env.isBrowserSupported
        console.log "The DYMO JS framework doesn't support this browser."
    else if not env.isFrameworkInstalled
        $el = $('#dymo-not-loaded')
        $el.html($el.data('error')).slideDown()
        # Show and log an error
        console.log "Make sure you gave permission for the DYMO browser plugin to run on this page. Try reloading the page if this message persists, or check page permissions."
        console.log "\t --> DYMO reports: #{env.errorDetails}"
        
        # Check whether we've OK'ed the DYMO plugin periodically
        recheck_dymo = ->
            if hestia.d.checkEnvironment().isFrameworkInstalled
                # We're good to go, show the success message, and kick off the app
                $el.addClass('success')
                $el.html($el.data('success'))
                setTimeout ->
                    $el.slideUp 'slow', ->
                        $el.removeClass('success')
                        # Move on the to the next step -- make sure we have a printer available
                        dymo_printer_check()
                , 2500
            else
                setTimeout(recheck_dymo, 500)
        recheck_dymo()
    else dymo_printer_check()

# Make sure there's actually a printer to use -- if not, show an error bar (if it hasn't already been shown)
dymo_printer_check = ->
    if not hestia.d.getPrinters().length > 0
        $el = $('#no-dymo-printer:hidden')
        $el.html($el.data('error')).slideDown()
    # We have a printer, let's get the label template, and start the app
    else
        $.get '/dymo-template', (data) -> hestia_start(data)

hestia_start = (label_template) ->

    # Verify all the required info, then print the label
    $('#submit').on 'click', (event) ->
        $name = $('input#name')
        name = $name.val()
        about = $('input#about').val()
        github = $('input#github-username').val()

        # No name, so show an error tooltip
        if not name.length > 0
            $tooltip = $('.row.name .tooltip')
            $tooltip.text $tooltip.data('error')
            $tooltip.addClass('show')

            # Keep checking for a name as the user types
            $name.off('blur keyup')
            $name.on 'blur keyup', ->
                if $name.val().length > 0
                    $tooltip.text $tooltip.data('success')
                    $tooltip.addClass('success')
                else
                    $tooltip.text $tooltip.data('error')
                    $tooltip.removeClass('success') 
        else
            # Log the user
            $.post '/logs',
                name: name,
                about: about,
                github: github
            # Define the printer and print options
            printer = hestia.d.getPrinters()[0]
            print_options = ''

            # Prepare the label
            template = $.parseXML label_template
            $template = $(template)

            # Find the <String> element in the template that has a matching <Name> tag
            find_label_string = (name) -> $("Name:contains('#{name}')", $template).parent().find('String')

            $label_name = find_label_string 'Name'
            $label_about = find_label_string 'About'
            $label_github = find_label_string 'GitHub'

            # Substitute all the values in the label template with user-supplied info
            $label_name.text(name)
            if about.length > 0 then $label_about.text(about) else $label_about.text('')
            # If we don't have a GitHub id, hide the GitHub logo
            if not github.length > 0
                $('Name:contains("GitHubImage")').closest('ObjectInfo').remove()
                $label_github.text('')
            else
                $label_github.text("@#{github}")
            
            # Debugging info if needed
            if hestia.debug then console.log 'Printer: ', printer, 'Print options: ', print_options, 'Label XML: ', $template

            # Render the template as a string
            label_as_str = (new XMLSerializer()).serializeToString(template)
            
            # Actually print the label
            if printer? and printer.name?
                hestia.d.printLabel(printer.name, print_options, label_as_str)
            else console.log 'Printer error: no DYMO printer found.'

###
# -------------------
# GitHub auto-fill magic
# -------------------
###

find_github_user = (name) ->
    $tooltip = $('.row.github .tooltip')
    $loading = $('.row.github .loading')
    $loading.addClass('show')

    $.getJSON "https://api.github.com/users/#{encodeURIComponent(name)}", (user) ->
        # If there was an form error before, tell the user it's been fixed
        if $tooltip.hasClass('show') and not $tooltip.hasClass('success')
            $tooltip.text($tooltip.data('success'))
            $tooltip.addClass('success')
            # Show the success message for three seconds, the hide it
            setTimeout ->
                if $tooltip.hasClass('success') # Make sure an error hasn't happened in the last three seconds
                    $tooltip.removeClass('show')
                    # Wait for the CSS transition to complete before dropping the class
                    setTimeout ->
                        $tooltip.removeClass('success')
                    , hestia.css_transition_duration
            , 3000

        # Fill in the user details
        if user.name?
            $('input#name').val(user.name)
        if user.company? and user.company.length > 0
            about = "Creator at #{user.company}"
        else
            about = "Creator"
        $('input#about').val(about)

        # Hide the loading indicator after briefly showing it
        setTimeout ->
            $loading.removeClass('show')
        , 500
    .error (event) ->
        # We couldn't find that GitHub user
        if event.status is 404
            $tooltip.removeClass('success')
            $tooltip.text($tooltip.data('error'))
            $tooltip.addClass('show')

            # Hide the loading indicator after briefly showing it
            setTimeout ->
                $loading.removeClass('show')
            , 500

        else
            console.log 'Error fetching GitHub user: ',event
