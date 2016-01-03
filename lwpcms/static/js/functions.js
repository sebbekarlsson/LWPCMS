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


function init_attachment_searchers() {
    /* Fetch all inputs. */
    inputs = document.querySelectorAll('.attachment-search');
    
    /* Iterate the fetched inputs. */
    for(var i = 0; i < inputs.length; i++) {
        /* Current input in the iteration. */
        input = inputs[i];
        
        /* Add keyup eventlistener to the current input. */
        input.addEventListener("keyup", function() {
            /*
             * !THIS HAPPENS ON "keyup" EVENT ON THE INPUT!
             */ 

            /* Query the attachments from database. */
            attachments = query_attachments(input.value)['attachments'];
            
            /* If we got attachments in the array, add a dropdown to parent. */
            if(attachments.length > 0) {
                /* Creating the dropdown element. */
                dropdown = document.createElement('select');
                
                /* Iterating the attachments. */
                for(var ii = 0; ii < attachments.length; ii++) {
                    /* Current attachment in iteration. */
                    attachment = attachments[ii];
                    
                    /* Creating select option element for current attachment. */
                    option = document.createElement('option');
                    option.setAttribute('value', attachment['id']);
                    option.innerHTML = attachment['content'];
                    
                    /* Appending the option to the dropdown. */
                    dropdown.appendChild(option);
                    
                    /* Adding a "click" eventlistener to the dropdown. */
                    dropdown.addEventListener("click", function(){
                        /* Fetching the hidden input element next to the attachment-search input. */
                        var input_hidden = input.parentNode.querySelector('input[type="hidden"]');
                        
                        /* Setting the value of the attachment-search input to the option data. (attachment title) */
                        input.value = dropdown.options[dropdown.selectedIndex].innerHTML;

                        /* Setting the value of the hidden input to the option value. (attachment id) */
                        input_hidden.value = dropdown.options[dropdown.selectedIndex].value;
                    });
                }
                
                /* Appending the dropdown to the inputs parent node. */
                input.parentNode.appendChild(dropdown);
            }
        });
        
        /*
         * WE WANT TO REMOVE THE DROPDOWN IF THE USER TRIES TO TYPE SOMETHING
         * ELSE.
         *
        /* Adding a "keydown" eventlistener to the input. */
        input.addEventListener("keydown", function() {
            /* Fetching all dropdowns in the same parent as the input. */
            dropdowns = input.parentNode.querySelectorAll('select');

            /* Iterating the dropdowns. */
            for(var ii = 0; ii < dropdowns.length; ii++) {
                /* Removing the current dropdown in the iteration. */
                input.parentNode.removeChild(dropdowns[ii]);
            }  
        });

        //input.setAttribute('init', 'true');
    }
}
