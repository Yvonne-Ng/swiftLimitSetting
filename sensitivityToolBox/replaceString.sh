#!/bin/bash
#Francesco Guescini

function freplaceInPDF() {
    if [[ $# -lt 3 ]]
    then
	echo
	echo "HELP: freplaceInPDF string-to-replace new-string /path/to/files/with/wildcard*"
    else
	echo -e "\nreplacing \"$1\" with \"$2\""
	for file in "${@: +3}" #do not use the first two arguments
	do
	    if [[ ! -e $file || ${file: -4} != ".pdf" ]]
	    then continue
	    fi
	    echo -e "$file"
	    pdftops -eps $file
	    sed -i -e "s/${1}/${2}/g" ${file%.pdf}.eps
	    epstopdf ${file%.pdf}.eps
	done
    fi
}

function freplaceInName() {
    if [[ $# -lt 3 ]]
    then
	echo
	echo "HELP: freplaceInName string-to-replace new-string /path/to/files/with/wildcard*"
    else
	echo -e "\nreplacing \"$1\" with \"$2\""
	for file in "${@: +3}" #do not use the first two arguments
	do
	    if [[ `echo $file|grep $1` ]] 
	    then
		echo "$file"
		mv -i $file "${file//$1/$2}"
	    fi
	done
    fi
}
