from flask import (
    Blueprint,
    render_template,
    abort, url_for,
    render_template_string
)
from lwpcms.api.themes import get_activated_theme
from lwpcms.mongo import db
import glob 


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)


@bp.route('/<template_name>')
def render(template_name):
    theme = get_activated_theme()
    
    if theme is not None:
        page_path = '{}/pages/{}'.format(theme['path'], template_name)

        posts = list(
                    db.collections.find(
                        {
                            'type': 'post',
                            'classes': ['post']
                        }
                    )
                )
        
        return render_template_string(open(page_path).read(), posts=posts)
    else:
        return render_template('index.html')
