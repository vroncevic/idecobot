#!/bin/bash
#
# @brief   idecobot
# @version 1.0.0
# @date    Mon Sep 21 08:30:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 coverage/ats_coverage.py idecobot
pylint idecobot > idecobot.report
echo "Done"
