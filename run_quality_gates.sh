#!/bin/bash
#
# @brief   idecobot
# @version 1.0.3
# @date    Mon Sep 21 08:30:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 gates/gates/interfaces_checker.py idecobot
python3 gates/gates/isp_checker.py idecobot
python3 gates/gates/limits_checker.py idecobot
python3 gates/gates/srp_checker.py idecobot

echo "Done"
