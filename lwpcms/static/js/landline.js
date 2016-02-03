function call(url, content_type) {
    var http = new XMLHttpRequest();

    http.open("GET", url, false);
    http.setRequestHeader("Content-type", content_type);
    http.send();

    return JSON.parse(http.responseText);
}


function landline_call() {
    var callers = document.querySelectorAll('*[call]');
    for (var i = 0; i < callers.length; i++) {
        caller = callers[i];

        var url = caller.getAttribute('call');
        var content_type = caller.getAttribute('content-type');
        var event = caller.getAttribute('event');

        if (content_type == undefined || content_type == null) {
            content_type = 'application/json';
        }

        if (event == undefined || event == null) {
            event = 'click';
        }


        caller.addEventListener(event, function(e) {
            var response = call(url, content_type);

            console.log(response);
        });
    }

    return true;
}
