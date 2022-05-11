#!/bin/bash

cd /home/boincadm/boinc_improved_fault_tolerance_and_integrity \
&& make \
&& echo "y" | ./tools/upgrade /home/boincadm/projects/gtcl \
&& cd /home/boincadm/projects/gtcl \
&& ./bin/start