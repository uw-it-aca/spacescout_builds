from fabric.api import local, prefix, prompt
from fabric.contrib.console import confirm
import random
import getpass
import pexpect
import sys
import fabric.utils


def deploy_dev():
    info = _get_user_info()
    for project in ["server", "admin", "web"]:
        child = pexpect.spawn("fab deploy_dev_%s" % project)
        child.logfile = sys.stdout
        
        # The timeout can be changed depending on connection/processor speed.
        child.expect("Would.*: ", timeout=None)
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
        
        if project is 'web' or project is 'admin':
            child.expect("I am about to install node.js.*?")
            child.sendline(info[3])
        
        child.expect(pexpect.EOF, timeout=None)


def deploy_dev_server():
    local("virtualenv --no-site-packages server_proj/")
    with prefix(". server_proj/bin/activate"):
        local("git clone git://github.com/uw-it-aca/spotseeker_server.git server_proj/spotseeker_server")
        local("pip install -r server_proj/spotseeker_server/requirements/requirements.txt")
        local("cp configs/dev/server_local_settings.py server_proj/server_proj/local_settings.py")
        local("cp server_proj/server_proj/sample.wsgi.py server_proj/server_proj/wsgi.py")
        _replace_local_settings_for("server_proj")
        with prefix("cd server_proj/"):
            local("python manage.py syncdb")
            local("python manage.py migrate")


def deploy_dev_admin():
    local("virtualenv --no-site-packages admin_proj/")
    with prefix(". admin_proj/bin/activate"):
        local("git clone git://github.com/uw-it-aca/spacescout_admin.git admin_proj/spacescout_admin")
        local("pip install -r admin_proj/spacescout_admin/requirements.txt")
        local("cp configs/dev/admin_local_settings.py admin_proj/admin_proj/local_settings.py")
        _replace_local_settings_for("admin_proj")
        with prefix("cd admin_proj/"):
            local("python manage.py syncdb")
    if local("which curl", capture=True) != '' and not 'darwin' in local('uname', capture=True).lower():
        with prefix("cd admin_proj/bin/"):
            local("wget https://raw.github.com/chuwy/nodeenv/master/nodeenv.py")
        install_node_js = confirm("I am about to install node.js for you.  It may take a long time, and it is possible to install it yourself.  Okay to proceed?")
        if install_node_js:
            with prefix(". admin_proj/bin/activate"):
                with prefix("python admin_proj/bin/nodeenv.py -p"):
                    local("npm install -g less")
        else:
            print('Skipping node.js install.  You must install it yourself for the admin app to work')
    else:
        if local("which curl", capture=True) == '':
            no_nodeenv_reason = " don't have curl installed "
        elif 'darwin' in local("uname", capture=True).lower():
            no_nodeenv_reason = ' are on a Mac '
        else:
            no_nodeenv_reason = ' are special '
        print("You" + no_nodeenv_reason + "so I can't install nodeenv.  You'll have to install node.js yourself.")


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
        local("git clone git://github.com/uw-it-aca/spacescout_web.git web_proj/spacescout_web")
        local("pip install -r web_proj/spacescout_web/base-requirements.txt")
        local("cp configs/dev/web_local_settings.py web_proj/web_proj/local_settings.py")
        local("cp web_proj/web_proj/sample.wsgi.py web_proj/web_proj/wsgi.py")
        _replace_local_settings_for("web_proj")
        with prefix("cd web_proj/"):
            local("python manage.py syncdb")
    if local("which curl", capture=True) != '' and not 'darwin' in local('uname', capture=True).lower():
        with prefix("cd web_proj/bin/"):
            local("wget https://raw.github.com/chuwy/nodeenv/master/nodeenv.py")
        install_node_js = confirm("I am about to install node.js for you.  It may take a long time, and it is possible to install it yourself.  Okay to proceed?")
        if install_node_js:
            with prefix(". web_proj/bin/activate"):
                with prefix("python web_proj/bin/nodeenv.py -p"):
                    local("npm install -g less")
        else:
            print('Skipping node.js install.  You must install it yourself for the web app to work')
    else:
        if local("which curl", capture=True) == '':
            no_nodeenv_reason = " don't have curl installed "
        elif 'darwin' in local("uname", capture=True).lower():
            no_nodeenv_reason = ' are on a Mac '
        else:
            no_nodeenv_reason = ' are special '
        print("You" + no_nodeenv_reason + "so I can't install nodeenv.  You'll have to install node.js yourself.")


def start_server():
    local('scripts/start_server.sh')


def start_admin():
    local('scripts/start_admin.sh')


def start_docs():
    local('scripts/start_docs.sh')


def start_web():
    local('scripts/start_web.sh')


def start_all():
    local('screen -c configs/screenrc')


def clean_all():
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
    print("The following information will facilitate the automatic creation of a superuser account for your Django project(s).")
    username = raw_input("Username: ")
    email = raw_input("E-mail address: ")
    pass1 = getpass.getpass("Password: ")
    pass2 = getpass.getpass("Password (again): ")
    while pass1 != pass2:
        print "Error: The passwords you typed do not match."
        pass1 = getpass.getpass("Password: ")
        pass2 = getpass.getpass("Password (again): ")
    install_node_js = prompt("The node.js install can take a long time and you can install it yourself.  Would you like me to do it automatically?", default='y').lower()[0]
    while install_node_js not in ['y', 'n']:
        install_node_js = prompt("I didn't understand you.  Do you want node.js installed?  Please say y or n", default='y').lower()[0]
    return [username, email, pass1, install_node_js]
