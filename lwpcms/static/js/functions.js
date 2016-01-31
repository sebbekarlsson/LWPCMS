/*
 * This will be converted to a more convincing httprequest library later.
*/
function query_attachments(query) {
    var http = new XMLHttpRequest();
    var url = "/api/query_attachments/" + query;

    http.open("GET", url, false);
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    http.send();

    return JSON.parse(http.responseText);
}


/*
 * This will be converted to a more convincing httprequest library later.
*/
function generate_testdata() {
    var http = new XMLHttpRequest();
    var url = "/api/generate_testdata";

    http.open("GET", url, false);
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    http.send();

    return JSON.parse(http.responseText);
}
