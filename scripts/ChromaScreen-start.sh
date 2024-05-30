#!/bin/bash

SCRIPTPATH=$(dirname $(realpath $0))
if [ -f $SCRIPTPATH/launch_ChromaScreen.sh ]
then
echo "Running "$SCRIPTPATH"/launch_ChromaScreen.sh"
$SCRIPTPATH/launch_ChromaScreen.sh
exit $?
fi

echo "Running ChromaScreen on X in display :0 by default"
/usr/bin/xinit $KS_XCLIENT
