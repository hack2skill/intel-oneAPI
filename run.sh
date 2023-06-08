#!/bin/bash

numactl --cpunodebind=0 --membind=0 python ./main.py