#!/usr/bin/env bash

LINES=$(grep "FAIL" test_output | wc -l)
if [[ "$LINES" -gt 0 ]]; then
    exit 1
fi