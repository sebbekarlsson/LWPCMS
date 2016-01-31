var backdrop = ElemenTailor.create(
        'div',
        {
            id: 'lwpcms-backdrop'
        }
        )
var window_manager_element = ElemenTailor.create(
            'div',
            {
                id: 'lwpcms-window-manager',
                childs:[
                    backdrop
                ]
            }
        );
backdrop.addEventListener('click', function (e) {
    var windows = document.querySelectorAll('.lwpcms-backdrop-window');

    for (var i = 0; i < windows.length; i++) {
        ElemenTailor.delete(windows[i]);
    }

    this.style.opacity = 0;
    this.style.zIndex = -30;
});

function lwpcms_window(waiter, title) {
    w = ElemenTailor.create(
        'div',
        {
            class: 'lwpcms-backdrop-window',
            childs: [
                ElemenTailor.create(
                    'div',
                    {
                        class: 'lwpcms-backdrop-window-top',
                        childs: [
                            ElemenTailor.create(
                                'ul',
                                {
                                    class: 'left',
                                    childs: [
                                        ElemenTailor.create(
                                            'li',
                                            {
                                                childs: [
                                                    ElemenTailor.create('label', {innerHTML: title})
                                                ]
                                            }
                                        )
                                    ]
                                }
                            ),
                             ElemenTailor.create(
                                'ul',
                                {
                                    class: 'right',
                                    childs: [
                                        ElemenTailor.create(
                                            'li',
                                            {
                                                childs: [
                                                    ElemenTailor.create(
                                                        'label',
                                                        {
                                                            childs: [
                                                                ElemenTailor.create(
                                                                    'object',
                                                                    {
                                                                        fill: 'white',
                                                                        data: '/static/image/close.svg',
                                                                        onerror: 'this.onerror=null' 
                                                                    }
                                                                )
                                                            ]
                                                        }
                                                    )
                                                ]
                                            }
                                        )
                                    ]
                                }
                            )
                        ]
                    }
                )
            ]
        }
    );


    w.addEventListener('DOMNodeRemoved', function(e) {
        waiter.setAttribute('window-response', w.innerHTML);
    });

    window_manager_element.appendChild(w);
    color_svgs();
   
    backdrop.style.zIndex = 20; 
    backdrop.style.opacity = 1;
}
