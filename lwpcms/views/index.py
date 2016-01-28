from flask import (
    Blueprint,
    render_template,
    abort, url_for,
    render_template_string
)
from lwpcms.api.themes import get_activated_theme
from lwpcms.mongo import db


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)


@bp.route('/')
def render():
    theme = get_activated_theme()
    
    if theme is not None:
        path = '{}/root_route/index.html'.format(theme['path'])
        
        posts = list(
                    db.collections.find(
                        {
                            'type': 'post',
                            'classes': ['post']
                        }
                    )
                )
        print(posts)
        

        return render_template_string(open(path).read(), posts=posts)
    else:
        return render_template('index.html')
