#!/bin/env bash
cd src && \
    python main.py \
    -m RELEASE \
    -u /dev/sdb \
    --execute-stage 1 \
    --execute-stage 2 \
    --execute-stage 3 \
    --execute-stage 4 \
    --execute-stage 5 \
    --execute-stage 6 \
    --execute-stage 7 \
    --execute-stage 8 \
    --execute-stage 9 \
    --execute-stage 10

