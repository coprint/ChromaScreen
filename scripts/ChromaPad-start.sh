#!/bin/bash

SCRIPTPATH=$(dirname $(realpath $0))
if [ -f $SCRIPTPATH/launch_ChromaPad.sh ]
then
echo "Running "$SCRIPTPATH"/launch_ChromaPad.sh"
$SCRIPTPATH/launch_ChromaPad.sh
exit $?
fi

echo "Running ChromaPad on X in display :0 by default"
/usr/bin/xinit $KS_XCLIENT
