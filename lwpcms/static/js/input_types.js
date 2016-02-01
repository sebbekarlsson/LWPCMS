var inputs = document.querySelectorAll('input');


function apply_inputs (input) {
    if (input != null) {
       var type = input.getAttribute('type');
        
        switch (type) {
            case 'lwpcms-file':
                    
                    var attachments = query_attachments('*')['attachments'];
                    console.log(attachments);
                    var options = [];

                    for (var i = 0; i < attachments.length; i++) {
                        options.push(
                            ElemenTailor.create(
                                'option',
                                {
                                    value: attachments[i].id,
                                    innerHTML: attachments[i].title
                                }
                            )
                        );
                    }
                    
                    input.value = 'Choose File';
                    input.setAttribute('readonly', true);
                    
                    input.addEventListener('click', function(e) {
                        e.preventDefault();
                        
                        lwpcms_window(
                            this,
                            'Choose File',
                            ElemenTailor.create(
                                'select',
                                {
                                    childs: options
                                }
                            ),
                            function(e, c) {
                                input.parentNode.appendChild(
                                    ElemenTailor.create(
                                        'label',
                                        {
                                            innerHTML: c.options[c.selectedIndex].value
                                        }
                                    )
                                );
                                input.parentNode.appendChild(
                                    ElemenTailor.create(
                                        'input',
                                        {
                                            type: 'hidden',
                                            name: 'attachment_id',
                                            value: c.options[c.selectedIndex].value
                                        }
                                    )
                                );
                                ElemenTailor.delete(input);
                            }
                        );
                    });

                    break;
        }

        return true;
    }

    for (var i=0; i< inputs.length; i++) {
        input = inputs[i];
        var type = input.getAttribute('type');
        
        switch (type) {
            case 'lwpcms-file':
                    input.value = 'Choose File';
                    input.setAttribute('readonly', true);
                    
                    input.addEventListener('click', function(e) {
                        e.preventDefault();

                        lwpcms_window(this, 'Choose File');
                    });

                    break;
        }
    }

    return true;
}
