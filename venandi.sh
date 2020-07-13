#!/bin/bash

if [ $# -lt 1 ]
then
	echo ""
	echo "This script will make the recon process less painful."
	echo "Happy Hunting :)"
	echo ""
	echo "Options:"
	echo "  -d, --domain		Specifies a domain"
	echo "  -o, --output		Outputs result to a file"
	echo ""
	exit 1
fi

while getopts ":d:o:" flag; do
  case "${flag}" in
	d) domain=${OPTARG} ;;
	o) output=${OPTARG} ;;
  esac 
done

function crt() {
	curl -s "https://crt.sh/?q=%.$domain&output=json" | jq -r '.[].name_value' | grep -v "\*" | sort | uniq | httprobe | grep "https" | tee /tmp/$domain/result
}

function sslmate() {
	curl -s "https://api.certspotter.com/v1/issuances?domain=$domain&include_subdomains=true&expand=dns_names" | jq -r '.[].dns_names[]' | grep -v "\*" | sort | uniq | httprobe | grep "https" | tee -a /tmp/$domain/result
}

function screenshot() {
	mkdir "/tmp/$domain/screenshot"
	cat /tmp/$domain/result | aquatone -out "/tmp/$domain/screenshot/"
}


check=$(host $domain | grep -m 1 handled | cut -d " " -f 3-4)
if [[ $check == "is handled" ]]
then
	mkdir /tmp/$domain/
	echo "Fetching from crt.sh..."
	echo ""
	crt
	echo ""
	echo "Results saved in /tmp/$domain/"
	echo "Fetching from certspotter..."
	echo ""
	sslmate
	echo ""
	echo "Results saved"
	echo "Taking screenshots..."
	echo ""
	screenshot
	echo ""
	echo "All tasks completed"
else
	echo ""
	echo "Invalid domain"
	echo ""
	exit 1
fi

