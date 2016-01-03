var addlists = document.querySelectorAll('.lwpcms-addlist');

function add_addlist_item(addlist, type) {
    switch(type) {
        case 'attachment':
            var item = document.createElement('div');
            item.className += 'lwpcms-addlist-item';

            var left_section = document.createElement('section');
            left_section.className += 'lwpcms-addlist-left';
            left_section.innerHTML = 'ADD';

            left_section.addEventListener("click", function(){
                add_addlist_item(addlist, type);
            });

            var right_section = document.createElement('section');
            right_section.className += 'lwpcms-addlist-right lwpcms-inputs';

            var input = document.createElement("input");
            input.setAttribute('type', 'text');
            input.className += 'attachment-search';
            right_section.appendChild(input);

            var input_hidden = document.createElement("input");
            input_hidden.setAttribute('type', 'hidden');
            input_hidden.setAttribute('name', 'attachment_id');
            right_section.appendChild(input_hidden);

            item.appendChild(left_section);
            item.appendChild(right_section);

            addlist.appendChild(item);
            break;
    }
}

for(var i = 0; i < addlists.length; i++) {
    addlist = addlists[i];
    type = addlist.getAttribute('type');
    
    add_addlist_item(addlist, type);
}
