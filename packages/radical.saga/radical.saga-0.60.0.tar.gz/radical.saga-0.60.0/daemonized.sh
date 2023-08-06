
set -e
atexit()
{
    echo "daemonized $$ $PPID `date` -- exit" >> /tmp/l
    exit
}
trap atexit INT TERM KILL

while true
do
    sleep 1
    echo "daemonized $$ $PPID `date`" >> /tmp/l
done

