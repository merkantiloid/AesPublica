from fabric.api import run, cd, settings

def deploy():
    code_dir = '/srv/django/myproject'

    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo/.git %s" % code_dir)

    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")