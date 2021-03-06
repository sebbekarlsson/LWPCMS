/*
 * This will be converted to a more convincing httprequest library later.
 */
function query_files(query, page, limit) {
    var http = new XMLHttpRequest();
    var url = "/api/query_files/" + query + '/' + page + '/' + limit;

    http.open("GET", url, false);
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    http.send();

    return JSON.parse(http.responseText);
}


/*
 * This will be converted to a more convincing httprequest library later.
 */
function query_data(query) {
    var http = new XMLHttpRequest();
    var url = "/api/query";

    http.open("POST", url, false);
    http.setRequestHeader("Content-type", "application/json");
    http.send(JSON.stringify(query));

    return JSON.parse(http.responseText);
}


/*
 * This will be converted to a more convincing httprequest library later.
 */
function remove_attachment(post_id, attach_id) {
    var http = new XMLHttpRequest();
    var url = `/api/remove_attachment/${post_id}/${attach_id}`;

    http.open("GET", url, false);
    http.setRequestHeader("Content-type", "application/json");
    http.send();

    return JSON.parse(http.responseText); 
}


/*
 * This will be converted to a more convincing httprequest library later.
 */
function delete_file(e, id) {
    var http = new XMLHttpRequest();
    var url = "/api/delete_file/" + id;

    http.open("GET", url, true);
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
            e.parentNode.parentNode.style.display = 'none';
        }
    }

    http.send();
}


/**
 * Used to fade in elements.
 * @param el <HTMLElement>
 * @param delta <Float>
 */
function lwpcms_fade_in(el, delta) {
    el.style.opacity = 0;

    var tick = function() {
        el.style.opacity = +el.style.opacity + delta;

        if (+el.style.opacity < 1) {
            (window.requestAnimationFrame && requestAnimationFrame(tick)) || setTimeout(tick, 16)
        }
    };

    tick();
}
