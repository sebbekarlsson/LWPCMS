var inputs = document.querySelectorAll('input');


function apply_inputs (input) {
    if (input != null) {
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
