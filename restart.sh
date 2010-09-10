#!/bin/sh
$HOME/AuPoil/bin/supervisorctl restart app1
sleep 3
$HOME/AuPoil/bin/supervisorctl restart app2
