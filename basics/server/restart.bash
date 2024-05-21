bash ./stop.bash

#nohup python3 -m flask --app flaskr run --debug >> log.log 2>&1 & echo $! > run.pid
nohup python3 -m flask --app flaskr run --debug >> log.log 2>&1 &
echo "Started server on pid $!"
