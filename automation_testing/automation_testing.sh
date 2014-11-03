#!/bin/bash
# automation_testing.sh : Set up and run automation tests for Spacescout
# Options
# -r     | --reset-databases       Delete and recreate django databases for each server
# -s     | --create-sample-spots   Create sample spots using the create_sample_spots command
# -c     | --create-consumer       Creates trusted consumer using create_consumer command and updates web_proj local_settings.py
# -v env | --virtualenv-dir env    Specifies an existing virtualenv. Otherwise one will be created

# Initialize variables
reset_databases="false"
create_sample_spot="false"
create_consumer="false"
virtualenv_dir="false"

# Initial flag value
ARG_B=0

# Read options
args=`getopt -o rscv: --long reset-databases,create-sample-spots,create-consumer,virtualenv-dir: -n 'automation_testing.sh' -- "$@"`
eval set -- "$args"

while true ; do
    case "$1" in
	-r|--reset-databases)
	    reset_databases="true" ;
	    shift
	    ;;
	-s|--create-sample-spots)
	    create_sample_spots="true" ;
	    shift
	    ;;
	-c|--create-consumer)
	    create_consumer="true" ;
	    shift
	    ;;
	-v|--virtualenv-dir)
	    case "$2" in
		"") virtualenv_dir='test_env' ; shift 2 ;;
		*) virtualenv_dir=$2 ; shift 2 ;;
	    esac ;;
	--) shift ; break ;;
	*) echo "option not found" l exit 1 ;;    
    esac
done

shift $((OPTIND-1))
[ "$1" = "--" ] && shift

# Reset databases
if [ "$reset_databases" == "true" ]
then
    ./input.expect $USER
fi

# Add sample spots and consumer
cd ../server_proj
. bin/activate

if [ "$create_sample_spots" == "true" ]
then
    python manage.py create_sample_spots --force-delete=yes
fi

if [ "$create_consumer" == "true" ]
then
    python manage.py create_consumer --name='TrustedConsumer' --trusted='yes' > consumerKey

    key=$(cat consumerKey | grep 'Key' | awk ' { print $2 } ')
    secret=$(cat consumerKey | grep 'Secret' | awk ' { print $2 } ')
    rm consumerKey

    cd ../web_proj/web_proj

    keyLine=$(grep -n 'SS_WEB_OAUTH_KEY' local_settings.py | awk ' { print $1 } ' FS=":")
    sed $keyline'd' local_settings.py

    secretLine=$(grep -n 'SS_WEB_OAUTH_SECRET' local_settings.py | awk ' { print $1 } ' FS=":")
    sed $secretLine'd' local_settings.py

    # awk -v n=$keyLine    -v s="SS_WEB_OAUTH_KEY = '$key'"       'NR == n {print s} {print}' local_settings.py > local_settings.py.new
    # awk -v n=$secretLine -v s="SS_WEB_OAUTH_SECRET = '$secret'" 'NR == n {print s} {print}' local_settings.py.new > local_settings.py.new.new
    # rm local_settings.py
    # mv local_settings.py{.new.new,}
    # rm local_settings.py.new

    echo "SS_WEB_OAUTH_KEY = '$key'" >> local_settings.py
    echo "SS_WEB_OAUTH_SECRET = '$secret'" >> local_settings.py

    cd ../../server_proj
fi

# Start all servers
cd ../scripts
./start_all_servers.sh
cd ../automation_testing

# Create virtualenv and run automation tests
$current_dir=$(pwd)
if [ "$virtualenv_dir" != "false" ]
then
    cd $virtualenv_dir
else
    mkdir test_env
    virtualenv test_env
    cd test_env
fi

# Start virtualenv and check for tools
. bin/activate
pip install selenium
pip install Pyvirtualdisplay

python ../../selenium/AcceptanceTests.py
deactivate
cd ..

if [ "$virtualenv_dir" == "false" ]
then
    rm -rf test_env
fi
