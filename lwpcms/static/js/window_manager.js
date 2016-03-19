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

    this.style.pointerEvents = 'none';
    this.style.opacity = 0;
    this.style.zIndex = -30;
});


function close_lwpcms_windows() {
    var backdrop = document.getElementById('lwpcms-backdrop');
    var windows = document.querySelectorAll('.lwpcms-backdrop-window');

    for (var i = 0; i < windows.length; i++) {
        ElemenTailor.delete(windows[i]);
    }

    backdrop.style.pointerEvents = 'none';
    backdrop.style.opacity = 0;
    backdrop.style.zIndex = -30; 
}


function lwpcms_window(waiter, title, content, action) {
    var button = ElemenTailor.create(
        'button',
        {
            class: 'lwpcms-btn',
            innerHTML: 'OK'
        }
    );

    var close_button = ElemenTailor.create(
        'label',
        {
            style: 'z-index: 35;\
                   position: absolute;\
                   top: 0;\
                   right: 8px;\
                   pointer-events: auto !important;\
                   ',
            class: 'clickable',
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
    );

    close_button.addEventListener('click', function(e) {
        close_lwpcms_windows();
    });

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
                                                    close_button
                                                ]
                                            }
                                        )
                                    ]
                                }
                            ) 
                        ]
                    }
                ),
                ElemenTailor.create(
                    'section',
                    {
                        class: 'lwpcms-bakdrop-window-content',
                        childs: [
                            content
                        ]
                    }
                ),
                ElemenTailor.create(
                    'section',
                    {
                        childs: [
                            button
                        ]
                    }
                )
            ]
        }
    );


    w.addEventListener('DOMNodeRemoved', function(e) {
        waiter.setAttribute('window-response', w.getAttribute('value'));
    });

    button.addEventListener('click', function(e) {
        if (action(e, content, w) == false) { close_lwpcms_windows(); }
    });
    
    var bounce = new Bounce();
    bounce.scale({
        from: {x: 0.1, y: 0.1},
        to: {x: 1, y: 1},
        duration: 2000 
    });
    bounce.applyTo(w);

    window_manager_element.appendChild(w);
    color_svgs();

    backdrop.style.pointerEvents = 'all';
    backdrop.style.zIndex = 20; 
    //backdrop.style.opacity = 1;
    lwpcms_fade_in(backdrop, 0.05);
}
