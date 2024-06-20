#!/bin/bash
cat ultima_version.csv |awk -F';' '{print $2 ";" $4 ";" $1}' >> inscritos_$(date +%Y).csv
