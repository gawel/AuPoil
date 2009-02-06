#!/bin/sh
bin/supervisorctl restart app1
sleep 3
bin/supervisorctl restart app2
