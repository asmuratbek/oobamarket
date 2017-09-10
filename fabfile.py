from fabric.api import cd, env, prefix, put, prompt, local, sudo, run, task, settings


PROJECT_NAME = 'ooba'
PROJECT_ROOT = '/home/admin/%s' % PROJECT_NAME
VENV_DIR = "/home/admin/ooba_env"
VENV_DEV_DIR = "/home/admin_dev/ooba_env"
REPO = 'git@bitbucket.org:monokbaev/oobamarket.git'
STAGING_NAME = 'oobamarket'
STAGING_ROOT = '/home/admin_dev/oobamarket'


env.hosts = ['176.31.28.85']
env.user = 'root'
env.password = '81Qm0yhhaSLd'


def update():
    with cd(PROJECT_ROOT):
        local('git pull {}'.format(REPO))
        with prefix('source ' + VENV_DIR + '/bin/activate'):
            run('pip install -r requirements/production.txt')
            run('./manage.py collectstatic --noinput')
            run('./manage.py migrate --settings=config.settings.prod')
            run('supervisorctl restart ooba_market')


def update_dev():
    with cd(STAGING_ROOT) and settings(user='admin_dev', password='sunrise226417'):
        local("git pull origin dev")
        with prefix('source ' + VENV_DEV_DIR + '/bin/activate'):
            run('pip install -r requirements/production.txt')
            run('./manage.py collectstatic --noinput')
            run('./manage.py migrate --settings=config.settings.dev')
            sudo('service supervisor stop')
            sudo('service supervisor start')
