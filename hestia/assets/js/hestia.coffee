---
---
# See documentation on the DYMO format in /docs
window.hestia = {
    debug : true,
}

hestia.layouts = {
    die_cut: """
<?xml version="1.0" encoding="utf-8"?>
<DieCutLabel Version="8.0" Units="twips">
    <PaperOrientation>Landscape</PaperOrientation>
    <Id>Address</Id>
    <PaperName>30252 Address</PaperName>
    <DrawCommands>
        <RoundRectangle X="0" Y="0" Width="1581" Height="5040" Rx="270" Ry="270" />
    </DrawCommands>
    <ObjectInfo>
        <TextObject>
            <Name>Text</Name>
            <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
            <BackColor Alpha="0" Red="255" Green="255" Blue="255" />
            <LinkedObjectName></LinkedObjectName>
            <Rotation>Rotation0</Rotation>
            <IsMirrored>False</IsMirrored>
            <IsVariable>True</IsVariable>
            <HorizontalAlignment>Left</HorizontalAlignment>
            <VerticalAlignment>Middle</VerticalAlignment>
            <TextFitMode>ShrinkToFit</TextFitMode>
            <UseFullFontHeight>True</UseFullFontHeight>
            <Verticalized>False</Verticalized>
            <StyledText>
                <Element>
                    <String>[empty text]</String>
                    <Attributes>
                        <Font Family="Open Sans" Size="22" Bold="True" Italic="False" Underline="False" Strikeout="False" />
                        <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />
                    </Attributes>
                </Element>
            </StyledText>
        </TextObject>
        <Bounds X="331" Y="150" Width="4560" Height="1343" />
    </ObjectInfo>
</DieCutLabel>
"""
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

    done_typing_interval = 1000 # for GH instant search, search once the user has stopped typing for this many milliseconds
    hestia.typing_timer = undefined
    hestia.search_timer = undefined
    $('input#github-username').on 'keyup', ->
        min_time_between = 12000 # GitHub requests without an authorized key are rate-limited to five requests per limit, or one request every 12 seconds
        clearTimeout(hestia.typing_timer)
        clearTimeout(hestia.search_timer)
        username = $('input#github-username').val()
        if username.length > 0
            # If the user has stopped typing for a sufficient amount of time, check that enough time has passed to make a GH request
            hestia.typing_timer = setTimeout ->
                console.log '3 seconds have passed'
                if hestia.last_gh_search?
                    # Calculate how much time has passed since the last search
                    ms_since_last = new Date() - hestia.last_gh_search
                    console.log ms_since_last / 1000, 's'
                    if ms_since_last > min_time_between # More than X seconds have pased
                        search_github(username)
                    else
                        # Set a timer for the remaining time, then run the search
                        console.log 'setting a timer for ',(min_time_between - ms_since_last)/1000,'s from now'
                        setTimeout ->
                            search_github(username)
                        , (min_time_between - ms_since_last)

                # This is our first GH search, no need to worry about intervals
                else search_github(username)
            , done_typing_interval


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

# Make sure there's actually a printer to use -- if not, show an error bar (if it hasn't already been shown)
dymo_printer_check = ->
    if not hestia.d.getPrinters().length > 0
        $el = $('#no-dymo-printer:hidden')
        $el.html($el.data('error')).slideDown()
    # We have a printer, we're good to go!
    else hestia_start()
    hestia_start()

hestia_start = ->
    # Verify all the required info, then print the label
    $('#submit').on 'click', (event) ->
        $name = $('input#name')
        name = $name.val()
        about = $('input#about').val()
        # No name, so show an error tooltipe
        if not name.length > 0
            $tooltip = $('.row.name .tooltip')
            $tooltip.text $tooltip.data('error')
            $tooltip.addClass('show')

            # Keep checking for a name as the user types
            $name.off('keyup')
            $name.on 'keyup', ->
                if $name.val().length > 0
                    $tooltip.text $tooltip.data('success')
                    $tooltip.addClass('success')
                else
                    $tooltip.text $tooltip.data('error')
                    $tooltip.removeClass('success') 
        else
            # Define the printer and print options
            printer = hestia.d.getPrinters()[0]
            print_options = ''

            # Prepare the label
            label = $.parseXML hestia.layouts.die_cut
            $label = $(label)
            $('String', $label).text("#{name}\n#{about}")
            label_as_str = (new XMLSerializer()).serializeToString(label)
            
            # Debugging info if needed
            if hestia.debug then console.log 'Printer: ', printer, 'Print options: ', print_options, 'Label XML: ', label

            # Actually print the label
            if printer? and printer.name?
                hestia.d.printLabel(printer.name, print_options, label_as_str)
            else console.log 'Printer error: no DYMO printer found.'

###
# -------------------
# GitHub auto-fill magic
# -------------------
###

search_github = (user) ->
    $.getJSON "https://api.github.com/search/users?q=#{encodeURIComponent(user)}+in:users", (data) ->
        hestia.last_gh_search = new Date()
        $list = $('#github-user-results')
        $list.empty()

        if data.items.length is 0
            $list.append("<li><p class='no-results'>No users found</p></li>")
        else
            for user in data.items[0..5]
                $list.append "<li><img src='#{user.avatar_url}'><p class='login'>#{user.login}</p></li>"
        $list.addClass('show')
