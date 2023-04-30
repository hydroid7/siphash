#!/usr/bin/env bash

LINES=$(grep "FAIL=0" ./test_output | wc -l)
if [[ "$LINES" -gt 0 ]]; then
    exit 0
else
    exit 1
fi