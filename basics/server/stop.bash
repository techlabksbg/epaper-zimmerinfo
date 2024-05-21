
for pid in `pidof python3`
do
	cmdline=`cat /proc/${pid}/cmdline | tr '\000' ' '`
	if [ "$cmdline" == "python3 -m flask --app flaskr run --debug " ]
	then
		echo "Found running server with pid $pid. Killing it..."
		kill $pid
	fi
done

