#!/bin/bash
. setup.sh
python generate_skeleton.py --destination_dir=$1 --csw_endpoint="$2"
