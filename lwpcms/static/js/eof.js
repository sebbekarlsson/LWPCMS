apply_inputs();

var content = document.getElementById('lwpcms-content');
content.appendChild(window_manager_element);

color_svgs();

var attachment_remove_buttons = document.querySelectorAll('.remove-attachment');
for(var i = 0; i < attachment_remove_buttons.length; i++) {
    remove_button = attachment_remove_buttons[i];

    remove_button.addEventListener('click', function(e) {
        e.preventDefault();

        var attach_id = this.parentNode.parentNode.querySelector('input[name="attachment_id"]').value;
        var post_id = document.querySelector('input[name="post_id"]').value;

        var data = remove_attachment(post_id, attach_id);
        if (data['status'] == 200) {
            ElemenTailor.delete(this.parentNode.parentNode.parentNode.parentNode);
        }
    });
}

landline_call();
