from fabric.api import cd, env, prefix, put, prompt, local, sudo, run


PROJECT_NAME = 'ooba'
PROJECT_ROOT = '/home/admin/%s' % PROJECT_NAME
VENV_DIR = "/home/admin/ooba_env"
REPO = 'git@bitbucket.org:monokbaev/oobamarket.git'


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
