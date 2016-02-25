var inputs = document.querySelectorAll('input');


function apply_inputs (input) {
    if (input != null) {
       var type = input.getAttribute('type');
        
        switch (type) {
            case 'lwpcms-file':
                    
                    var attachments = query_attachments('*')['attachments'];
                    var gallery_items = [];

                    for (var i = 0; i < attachments.length; i++) {
                        var ext = attachments[i].content.split('.')[1];
                        var fname = attachments[i].content.split('.')[0];
                        var attach_thumb = fname + '_128x128.' + ext;

                        var gallery_item = ElemenTailor.create(
                            'div',
                            {
                                attachment_id: attachments[i].id,
                                attachment_original: attachments[i].original,
                                attachment_title: attachments[i].title,
                                attachment_file: attachments[i].content,
                                class: 'lwpcms-gallery-item',
                                childs:[
                                    ElemenTailor.create(
                                        'p',
                                        {
                                            innerHTML: attachments[i].title
                                        }
                                    ),
                                    ElemenTailor.create(
                                        'img',
                                        {
                                            src: `/static/upload/${attach_thumb}`
                                        }
                                    )
                                ]
                            }
                        );
                        
                        gallery_item.addEventListener('click', function (e) {
                            var other_items = this.parentNode.querySelectorAll('.lwpcms-gallery-item');

                            for(var i = 0; i < other_items.length; i++) {
                                other_items[i].removeAttribute('selected');
                            }

                            this.setAttribute('selected', true);
                        });

                        gallery_items.push(gallery_item);
                    }
                    
                    input.value = 'Choose File';
                    input.setAttribute('readonly', true);
                    
                    input.addEventListener('click', function(e) {
                        e.preventDefault();
                        
                        lwpcms_window(
                            this,
                            'Choose File',
                            ElemenTailor.create(
                                'div',
                                {
                                    class: 'lwpcms-gallery',
                                    childs: gallery_items
                                }
                            ),
                            function(e, c, w) {
                                var attachment = c.querySelector('.lwpcms-gallery-item[selected="true"]');
                                var img_src = attachment.getElementsByTagName('img')[0].getAttribute('src');
                                
                                var remove_button = ElemenTailor.create(
                                    'button',
                                    {
                                        innerHTML: 'X',
                                        class: 'lwpcms-gallery-item-bar-btn warning'
                                    }
                                );

                                var item_bar = ElemenTailor.create('div', {
                                    class: 'lwpcms-gallery-item-bar',
                                    childs: [
                                        remove_button 
                                    ]
                                });

                                remove_button.addEventListener('click', function(e) {
                                    e.preventDefault();

                                    ElemenTailor.delete(this.parentNode.parentNode);
                                });


                                var gallery_item = ElemenTailor.create(
                                    'div',
                                    {
                                        class: 'lwpcms-gallery-item',
                                        childs:[
                                            item_bar,
                                            ElemenTailor.create(
                                                'p',
                                                {
                                                    innerHTML: attachment.getAttribute('attachment_original')
                                                }
                                            ),
                                            ElemenTailor.create(
                                                'img',
                                                {
                                                    src: img_src
                                                }
                                            ),
                                            ElemenTailor.create(
                                                'input',
                                                {
                                                    type: 'hidden',
                                                    name: 'attachment_id',
                                                    value: attachment.getAttribute('attachment_id')
                                                }
                                            )
                                        ]
                                    }
                                );

                                input.parentNode.parentNode.appendChild(gallery_item);
                                ElemenTailor.delete(input.parentNode);

                                close_lwpcms_windows();
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
