#!/bin/bash
. setup.sh
python generate_sitemap.py --destination_dir=$1 --csw_endpoint="$2"
