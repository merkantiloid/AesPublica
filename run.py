#!aes-env/bin/python3
from app import create_app

mainApp = create_app()
mainApp.jinja_env.auto_reload = True
mainApp.config['TEMPLATES_AUTO_RELOAD'] = True
mainApp.run(debug=True)
