from fabric.api import local, prefix

def deploy_dev_server():
    # server
    local("virtualenv --no-site-packages server_proj/")
    with prefix(". server_proj/bin/activate"):
        local("git clone git://github.com/abztrakt/spotseeker_server.git server_proj/spotseeker_server")
        local("pip install -r server_proj/spotseeker_server/requirements.txt")
    
    # admin
    local("virtualenv --no-site-packages admin_proj/")
    with prefix(". server_proj/bin/activate"):
        local("git clone git://github.com/abztrakt/spotseeker_admin.git admin_proj/spotseeker_admin")
        local("pip install -r admin_proj/spotseeker_admin/requirements.txt")
    
    # docs
    local("virtualenv --no-site-packages docs_proj/")
    with prefix(". docs_proj/bin/activate"):
        local("git clone git://github.com/abztrakt/spotseeker_docs.git docs_proj/spotseeker_docs")
        local("pip install -r docs_proj/spotseeker_docs/requirements.txt")
    
    # web
    local("virtualenv --no-site-packages web_proj/")
    with prefix(". docs_proj/bin/activate"):
        local("git clone git://github.com/abztrakt/spotseeker_web.git web_proj/spotseeker_web")
        local("pip install -r web_proj/spotseeker_web/requirements.txt")
