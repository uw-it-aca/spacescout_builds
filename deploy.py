import getopt
import getpass
import pexpect
import sys


__doc__ = """
Wrapper script for the Fabric script that handles deploying all SpaceScout projects. Script-ception.

Usage: python deploy.py [options]
Example: python deploy.py -h

Options:
    -h, --help       Get help
    --dev            Deploys dev admin, docs, server, and web.
    --dev-server     Deploys dev server
    --dev-admin      Deploys dev admin
    --dev-docs       Deploys dev docs
    --dev-web        Deploys dev web
    --clean          Cleans spacescout_builds
"""


def main():
    try:
        long_args = [
            'help',
            'dev',
            'dev-server',
            'dev-admin',
            'dev-docs',
            'dev-web',
            'clean',
        ]
        options, args = getopt.getopt(sys.argv[1:], 'h', long_args)
    except getopt.error, msg:
        print msg
        print "for help use -h or --help"
        sys.exit(2)
    for o, a in options:
        if o in ("-h", "--help", "help"):
            print __doc__
            sys.exit(0)
        if o == "--dev":
            print "Deploying all dev projects..."
            info = _get_user_info()
            deploy("server", info)
            deploy("admin", info)
            deploy("docs", info)
            deploy("web", info)
            print "Done."
        elif o == "--dev-server":
            info = _get_user_info()
            deploy("server", info)
            print "Done."
        elif o == "--dev-admin":
            info = _get_user_info()
            deploy("admin", info)
            print "Done."
        elif o == "--dev-docs":
            info = _get_user_info()
            deploy("docs", info)
            print "Done."
        elif o == "--dev-web":
            info = _get_user_info()
            deploy("web")
            print "Done."
        elif o == "--clean":
            response = raw_input("ALL uncommitted changes will be lost. Continue? (y/n): ")
            if response == "y": 
                child = pexpect.spawn("fab full_clean")
                child.expect("ALL.* ")
                child.sendline("y")
                child.expect(pexpect.EOF, timeout=None)
            

def deploy(project, info):
    print "Deploying dev %s..." % project
    child = pexpect.spawn("fab deploy_dev_%s" % project)
    child.expect("Would.*: ", timeout=120)      # Timeout can be changed depending on connection speed.
    child.sendline("yes")
    child.expect("Username.*: ")
    child.sendline("%s" % info[0])
    child.expect("E-mail.*: ")
    child.sendline("%s" % info[1])
    child.expect("Password.*: ")
    child.sendline("%s" % info[2])
    child.expect("Password.*: ")
    child.sendline("%s" % info[2])
    child.expect(pexpect.EOF, timeout=None)
    print "Finished dev %s." % project


def _get_user_info():
    print("The follow information will facilitate the automatic creation of a superuser account " + 
          "for your Django project(s).")
    username = raw_input("Username: ")
    email = raw_input("E-mail address: ")
    pass1 = getpass.getpass("Password: ")
    pass2 = getpass.getpass("Password (again): ")
    while pass1 != pass2:
        print "The passwords you typed do not match. Try again."
        pass1 = getpass.getpass("Password: ")
        pass2 = getpass.getpass("Password (again): ")
    return [username, email, pass1]
    

if __name__ == "__main__":
    main()
