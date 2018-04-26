#!/bin/bash

cat $1 | grep "ExecutionReport |" | grep -v EXEC_TYPE_PENDING | sed -n 's/.*exec_type=\([A-Z_]*\).*time_sent=\([0-9]*\).*received_from_exchange=\([0-9]*\).*order_received_oc=\([0-9]*\).*time_sent_exchange=\([0-9]*\).*/\1,\2,\3,\4,\5/p' | python ~/bin/octimes.py
