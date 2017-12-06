#!aes-env/bin/python3
from app import mainApp
mainApp.jinja_env.auto_reload = True
mainApp.config['TEMPLATES_AUTO_RELOAD'] = True
mainApp.run(debug=True)