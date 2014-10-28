#!/bin/sh
# start_all_servers.sh : Starts all Spacescout servers

for name in server admin web
do
echo $name
x-terminal-emulator --title=$name -e ./start_$name.sh --working-directory=.
done
