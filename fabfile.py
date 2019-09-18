from fabric import task
from invoke import Responder

from _credentials import github_password, github_username


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    project_root_path = '~/apps/django-blog-project/'

    # 进入项目根目录，从 Git 拉取最新代码，更新镜像
    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

        cmd = 'docker-compose -f production.yml up --build -d'
        c.run(cmd)
