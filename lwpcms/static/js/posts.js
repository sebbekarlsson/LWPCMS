/*
 * This will be converted to a more convincing httprequest library later.
*/
function delete_post(e, id) {
    var http = new XMLHttpRequest();
    var url = "/api/delete_post/" + id;

    http.open("GET", url, true);
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
            e.parentNode.parentNode.parentNode.parentNode.style.display = 'none';
        }
    }

    http.send();
}
