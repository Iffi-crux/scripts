#!/bin/bash

# Configuration
NAMESERVER="z.hackycorp.com"
ZONE="int"

echo "[*] Target Nameserver: $NAMESERVER"
echo "[*] Target Zone: $ZONE"
echo "[*] Attempting Zone Transfer (AXFR)..."
echo "--------------------------------------------------"

# Run dig with the axfr flag
# @$NAMESERVER tells dig which server to query
# $ZONE is the domain we want records for
dig @$NAMESERVER axfr $ZONE

echo "--------------------------------------------------"
echo "[*] Transfer attempt complete. Check output for 'Transfer failed' or a list of records."
