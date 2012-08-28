from fabric.api import local, prefix

def deploy_dev_server():
    local("virtualenv --no-site-packages server_proj/")
    with prefix("source server_proj/bin/activate"):
        local("git clone git://github.com/abztrakt/spotseeker_server.git")
        local("pip install -r server_proj/spotseeker_server/requirements.txt")
