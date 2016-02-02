var addlists = document.querySelectorAll('.lwpcms-addlist');

for (var i = 0; i < addlists.length; i++) {
    var addlist = addlists[i];
    var type = addlist.getAttribute('type') 

    var button_add = ElemenTailor.create('button',
        {
            class: 'lwpcms-btn',
            innerHTML: 'Add'
        }
    );

    button_add.addEventListener('click', function(e) {
        e.preventDefault();
        var section_items =
            this.parentNode.parentNode.querySelector('.lwpcms-addlist-items');
        

        var input_field = ElemenTailor.create('input', {type: type});
        apply_inputs(input_field);

        var item = ElemenTailor.create(
            'div',
            {
                class: 'lwpcms-addlist-item',
                childs:[
                    input_field
                ]
            }
        );

        section_items.appendChild(item);
    });

    var section_options = ElemenTailor.create('section', {
        class: 'lwpcms-addlist-options',
        childs: [
            button_add   
        ]
    });

    var section_items = ElemenTailor.create('section',
            {class: 'lwpcms-addlist-items'});

    addlist.appendChild(section_items);
    addlist.appendChild(section_options);
}
