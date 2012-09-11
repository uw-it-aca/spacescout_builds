from fabric.api import local, prefix
from fabric.contrib.console import confirm
import random
import getpass
import pexpect
import sys
import time


def deploy_dev():
    info = _get_user_info()
    for project in ["server", "admin", "docs", "web"]:
        child = pexpect.spawn("fab deploy_dev_%s" % project)
        child.logfile = sys.stdout
        
        # The timeout can be changed depending on connection/processor speed.
        child.expect("Would.*: ", timeout=300)
        child.sendline("yes")
        
        child.expect("Username.*: ")
        child.sendline(info[0])
        
        child.expect("E-mail.*: ")
        child.sendline(info[1])
        
        # Turn off log during password prompt.
        child.logfile = None
        child.expect("Password.*: ")
        child.sendline(info[2])
        
        child.expect("Password.*: ")
        child.sendline(info[2])
        child.logfile = sys.stdout
        
        child.expect(pexpect.EOF, timeout=None)


def deploy_dev_server():
    local("virtualenv --no-site-packages server_proj/")
    with prefix(". server_proj/bin/activate"):
        local("git clone git://github.com/abztrakt/spotseeker_server.git server_proj/spotseeker_server")
        local("pip install -r server_proj/spotseeker_server/requirements.txt")
        local("cp configs/dev/server_local_settings.py server_proj/server_proj/local_settings.py")
        _replace_local_settings_for("server_proj")
        with prefix("cd server_proj/"):
            local("python manage.py syncdb")
            local("python manage.py migrate")


def deploy_dev_admin():
    local("virtualenv --no-site-packages admin_proj/")
    with prefix(". admin_proj/bin/activate"):
        local("git clone git://github.com/abztrakt/spacescout_admin.git admin_proj/spacescout_admin")
        local("pip install -r admin_proj/spacescout_admin/requirements.txt")
        local("cp configs/dev/admin_local_settings.py admin_proj/admin_proj/local_settings.py")
        _replace_local_settings_for("admin_proj")
        with prefix("cd admin_proj/"):
            local("python manage.py syncdb")


def deploy_dev_docs():
    local("virtualenv --no-site-packages docs_proj/")
    with prefix(". docs_proj/bin/activate"):
        local("git clone git://github.com/abztrakt/spacescout_docs.git docs_proj/spacescout_docs")
        local("pip install -r docs_proj/spacescout_docs/requirements.txt")
        local("cp configs/dev/docs_local_settings.py docs_proj/docs_proj/local_settings.py")
        _replace_local_settings_for("docs_proj")
        with prefix("cd docs_proj/"):
            local("python manage.py syncdb")


def deploy_dev_web():
    local("virtualenv --no-site-packages web_proj/")
    with prefix(". web_proj/bin/activate"):
        local("git clone git://github.com/abztrakt/spacescout_web.git web_proj/spacescout_web")
        local("pip install -r web_proj/spacescout_web/requirements.txt")
        local("cp configs/dev/web_local_settings.py web_proj/web_proj/local_settings.py")
        _replace_local_settings_for("web_proj")
        with prefix("cd web_proj/"):
            local("python manage.py syncdb")


def full_clean():
    if confirm("ALL uncommitted changes will be lost. Continue?", default=False):
        local('git reset --hard')
        local('git clean -df')
        local('find . -name "*.pyc" -exec rm -rf {} \;')
        local('find . -name "*.db" -exec rm -rf {} \;')
        local('find . -name "local_settings.py" -exec rm -rf {} \;')
        local('rm -rf admin_proj/spacescout_admin')
        local('rm -rf docs_proj/spacescout_docs')
        local('rm -rf server_proj/spotseeker_server')
        local('rm -rf web_proj/spacescout_web')
        for proj in ['admin_proj', 'docs_proj', 'server_proj', 'web_proj']:
            local("rm -rf %s/bin" % proj)
            local("rm -rf %s/include" % proj)
            local("rm -rf %s/lib" % proj)


def _replace_local_settings_for(folder):
    secret_key = _generate_secret_key()
    f1 = open("%s/%s/local_settings.py" % (folder, folder), 'r')
    temp = f1.read()
    f1.close()
    local_settings = temp.replace("SECRET_KEY = ''", "SECRET_KEY = '%s'" % secret_key)
    f2 = open("%s/%s/local_settings.py" % (folder, folder), 'w')
    f2.write(local_settings)
    f2.close()


def _generate_secret_key():
    return "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])


def _get_user_info():
    print("The follow information will facilitate the automatic creation of a superuser account " +
          "for your Django project(s).")
    username = raw_input("Username: ")
    email = raw_input("E-mail address: ")
    pass1 = getpass.getpass("Password: ")
    pass2 = getpass.getpass("Password (again): ")
    while pass1 != pass2:
        print "Error: The passwords you typed do not match."
        pass1 = getpass.getpass("Password: ")
        pass2 = getpass.getpass("Password (again): ")
    return [username, email, pass1]
