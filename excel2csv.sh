#!/bin/bash
cat ultima_version.csv |awk -F';' '{print $1 ";" $3}' >> inscritos_$(date +%Y).csv
