#!/bin/bash
#Francesco Guescini

if [[ $# -ne 1 ]]
    then {
	echo
	echo "search-duplicate-events.sh"
	echo "HOW TO: ./search-duplicate-events.sh /path/to/file.event.lists"
	exit
    }
fi
list=$1
if [[ $list == *"lumiBlock"* ]]
then
    #data
    echo "      #    run    event    lumiBlock"
    logfile=${list%.runNumber-eventNumber-lumiBlock.list}
else
    #MC
    echo "      #    mcChannelNumber    run    event"
    logfile=${list%.mcChannelNumber-runNumber-eventNumber.list}
fi

logfile=${logfile##*/}
logfile=$logfile".log"
#less $list|sort|uniq -cd
less $list|sort|uniq -cd>log/$logfile
cat log/$logfile
