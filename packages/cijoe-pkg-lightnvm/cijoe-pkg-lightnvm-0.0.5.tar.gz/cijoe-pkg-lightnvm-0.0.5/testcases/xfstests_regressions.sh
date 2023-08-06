#!/bin/bash
#
# Verify that xfstests generic/127 run without error
#
# These xftests are have previously triggered bugs in PBLK
#
CIJ_TEST_NAME=$(basename "${BASH_SOURCE[0]}")
export CIJ_TEST_NAME
# shellcheck source=modules/cijoe.sh
source "$CIJ_ROOT/modules/cijoe.sh"
test::enter
test::require block

if ! xfstests::prepare; then
   test::fail "Failed to prepare for test"
fi

if ! xfstests::run "generic/127"; then
   xfstests::cleanup
   test::fail "At least one xfs test failed"
fi

xfstests::cleanup

test::pass
