from fabric.api import cd, env, prefix, put, prompt, local, sudo, run, task, settings


PROJECT_NAME = 'ooba'
PROJECT_ROOT = '/home/admin/%s' % PROJECT_NAME
VENV_DIR = "/home/admin/ooba_env"
VENV_DEV_DIR = "/home/admin_dev/ooba_env"
REPO = 'git@bitbucket.org:monokbaev/oobamarket.git'
STAGING_NAME = 'oobamarket'
STAGING_ROOT = '/home/admin_dev/oobamarket'


def update():
    env.host_string = '176.31.28.85'
    env.user = 'admin'
    env.password = 'sunrise226417'
    with cd(PROJECT_ROOT):
        run('git pull origin master')
        with prefix('source ' + VENV_DIR + '/bin/activate'):
            run('pip install -r requirements/production.txt')
            run('./manage.py collectstatic --noinput')
            run('./manage.py migrate --settings=config.settings.prod')
            sudo('supervisorctl restart ooba_market')


def update_dev():
    env.host_string = '145.239.33.4'
    env.user = 'admin_dev'
    env.password = 'sunrise226417'
    with cd(STAGING_ROOT):
        run("git pull origin dev")
        with prefix('source ' + VENV_DEV_DIR + '/bin/activate'):
            run('pip install -r requirements/production.txt')
            run('./manage.py collectstatic --noinput')
            run('./manage.py migrate --settings=config.settings.dev')
            sudo('service supervisor stop')
            sudo('service supervisor start')
