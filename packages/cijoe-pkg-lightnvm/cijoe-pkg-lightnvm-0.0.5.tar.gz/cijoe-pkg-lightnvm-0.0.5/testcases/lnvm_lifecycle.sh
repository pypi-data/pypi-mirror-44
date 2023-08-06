#!/bin/bash
#
# Verify that PBLK create/remove/recovery works
#
# This test runs trough a factory-create, remove, recover, remove sequence
#
CIJ_TEST_NAME=$(basename "${BASH_SOURCE[0]}")
export CIJ_TEST_NAME
# shellcheck source=modules/cijoe.sh
source "$CIJ_ROOT/modules/cijoe.sh"
test::enter
test::require nvme

if ! lnvm::create; then
  test::fail
fi

if ! lnvm::remove; then
  test::fail
fi

if ! lnvm::recover; then
  test::fail
fi

if ! lnvm::remove; then
  test::fail
fi

test::pass
