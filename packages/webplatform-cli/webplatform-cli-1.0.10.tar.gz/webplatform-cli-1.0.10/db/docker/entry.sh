#!/bin/bash -x 
#echo 0 | tee /proc/sys/vm/zone_reclaim_mode
#sysctl -w vm.zone_reclaim_mode=0
#numactl --interleave=all mongod --config /home/container/config/conf.yaml
# numa='numactl --interleave=all'
# if $numa true &> /dev/null; then
#    set -- $numa "$@"
# fi
mongod --config /home/container/config/conf.yaml
bash
