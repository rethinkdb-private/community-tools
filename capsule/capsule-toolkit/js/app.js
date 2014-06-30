GITHUB_TOKEN = '3df11993e5fa5e4b0c661b7abc965345f028c04d'
STACKLEAD_TOKEN = 'ce16e873ff'
button = "<ul class='pageActions'><li class='menu' id='rdb-toolkit'><span>Fetch details</span></li></ul>"

function generate_uuid(){
    var d = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x7|0x8)).toString(16);
    });
    return uuid;
};

show_toolkit = function() {
    $b = $(button)
    $('#pageNavWrapper').prepend($b);

    $b.on('click', function(e) {
        $email = $('span#party\\:emailPanel input');
        email = $email

        token = generate_uuid()
        if (email.length > 0) {
            $.ajax('http://localhost:5000/stacklead/request?email='+email+'&token='+token, function(response) {
                console.log('StackLead',response);
            });
            // long polling here
        }

        $github = $('span#party\\:webAddressPanel span.input:has(select option[value="GITHUB"][selected="selected"]) input');
        github = $github.val();
        console.log(github);
        if (github.length > 0) {
            $.getJSON('https://api.github.com/users/'+github, function(response) {
                console.log('GitHub',response);
            });
        }

    });
}


if (document.URL.indexOf('https://rethinkdb.capsulecrm.com/party/') != -1 && document.URL.indexOf('edit') != -1) {
    show_toolkit();
}
