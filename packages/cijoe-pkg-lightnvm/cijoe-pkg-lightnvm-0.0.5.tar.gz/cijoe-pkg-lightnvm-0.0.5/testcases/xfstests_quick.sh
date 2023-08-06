#!/bin/bash
#
# Verify that xfstests -g quick run without error
#
# Verify that xfstests -g quick run without error
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

if ! xfstests::run "-g quick"; then
   xfstests::cleanup
   test::fail "At least one xfs test failed"
fi

xfstests::cleanup

test::pass
