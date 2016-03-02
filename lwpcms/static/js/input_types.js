function create_gallery_items(files) {
    var gallery_items = [];

    for (var i = 0; i < files.length; i++) {
        var ext = files[i].content.split('.')[1];
        var fname = files[i].content.split('.')[0];
        var file_thumb = fname + '_128x128.' + ext;

        var gallery_item = ElemenTailor.create(
            'div',
            {
                file_id: files[i].id,
                file_original: files[i].original,
                file_title: files[i].title,
                file_file: files[i].content,
                class: 'lwpcms-gallery-item',
                childs:[
                    ElemenTailor.create(
                        'p',
                        {
                            innerHTML: files[i].title
                        }
                    ),
                    ElemenTailor.create(
                        'img',
                        {
                            src: '/static/upload/' + file_thumb
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
    
    return gallery_items;
}


function create_pager(filecount, per_page) {
    var pager_buttons = [];
    for (var i = 0; i < filecount/per_page; i++) {
        var pager_btn = ElemenTailor.create('a', {
            innerHTML: i,
            value: i,
            class: 'lwpcms-pager-btn'
        });

        pager_btn.addEventListener('click', function (e) {
            var this_parent = this.parentNode.parentNode;
            var gallery = this_parent.querySelector('#fetched_files');
            var value = this.getAttribute('value');

            var files = query_files('*', value, per_page)['files'];
            var gallery_items = create_gallery_items(files);

            gallery.innerHTML = '';

            for (var i = 0; i < gallery_items.length; i++) {
                item = gallery_items[i];
                gallery.appendChild(item);
            }

        });

        pager_buttons.push(pager_btn);
    }
    var pagers_holder = ElemenTailor.create('nav', {
        class: 'lwpcms-pager',
        childs: pager_buttons
    });

    return pagers_holder;
}


function apply_inputs (input) {
    if (input != undefined) {
       var type = input.getAttribute('type');
        
        switch (type) {
            case 'lwpcms-file':
                    
                    var filecount = query_files('*', -1, -1)['files'].length;
                    var per_page = 64;

                    var files = query_files('*', 0, per_page)['files'];
                    var gallery_items = create_gallery_items(files);

                   
                    if (filecount >= per_page) { 
                        pagers_holder_1 = create_pager(filecount, per_page);
                        pagers_holder_2 = create_pager(filecount, per_page);
                    } else {
                        pagers_holder_1 = ElemenTailor.create('span');
                        pagers_holder_2 = ElemenTailor.create('span');
                    }
                       
                    
                    input.value = 'Choose File';
                    input.setAttribute('readonly', true);
                    
                    input.addEventListener('click', function(e) {
                        e.preventDefault();
                        
                        lwpcms_window(
                            this,
                            'Choose File',
                            ElemenTailor.create('section', 
                                {
                                        childs:[
                                            pagers_holder_1,
                                            ElemenTailor.create(
                                                'div',
                                                {
                                                    class: 'lwpcms-gallery',
                                                    id: 'fetched_files',
                                                    childs: gallery_items
                                                }
                                            ),
                                            pagers_holder_2
                                        ]
                                }
                            ),
                            function(e, c, w) {
                                var file = c.querySelector('.lwpcms-gallery-item[selected="true"]');
                                var img_src = file.getElementsByTagName('img')[0].getAttribute('src');
                                
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
                                                    innerHTML: file.getAttribute('file_original')
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
                                                    name: 'file_id',
                                                    value: file.getAttribute('file_id')
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
    } else {
        var inputs = document.querySelectorAll('input');

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

                case 'tags':
                    var tags_section = input.parentNode.querySelector('lwpcms-tags-section');

                    if (tags_section == null) {
                        var tags_section = ElemenTailor.create('section', {
                            class: 'lwpcms-tags-section'
                        });
                        input.parentNode.appendChild(tags_section);
                    }
                    
                    if (input.getAttribute('tags') != null)
                    var tags = input.getAttribute('tags').split(',');

                    if(tags) {
                        for (var ii = 0; ii < tags.length; ii++) {

                            if (tags[ii] != '') {
                                var tag_element = ElemenTailor.create('input', {
                                    name: 'lwpcms_tag',
                                    class: 'lwpcms-tags-section-tag',
                                    value: tags[ii].replace(' ', '')
                                });

                                tag_element.addEventListener('click', function (e) {
                                    ElemenTailor.delete(this);
                                });

                                tags_section.appendChild(tag_element);
                            }
                        }
                    }

                    input.addEventListener('keyup', function(e) {
                        if (e.keyCode == 32) {
                            var text = this.value;
                            var new_tag = text.split(',')[text.split(',').length-2].replace(' ', '');

                            var tag_element = ElemenTailor.create('input', {
                                name: 'lwpcms_tag',
                                class: 'lwpcms-tags-section-tag',
                                value: new_tag
                            });

                            tag_element.addEventListener('click', function (e) {
                                ElemenTailor.delete(this);
                            });

                            tags_section.appendChild(tag_element);
                        }
                    });

                break;
            }
        }
    }

    return true;
}
