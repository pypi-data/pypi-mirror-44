#!/bin/bash
#
# Verify liblightnvm -- OCSSD 1.2/2.0 identify -- via `nvm_dev info`
#
# This is super simply check that it the device is able to identify
#
# shellcheck disable=SC2119
#
CIJ_TEST_NAME=$(basename "${BASH_SOURCE[0]}")
export CIJ_TEST_NAME
# shellcheck source=modules/cijoe.sh
source "$CIJ_ROOT/modules/cijoe.sh"
test::enter

if ! ssh::cmd "NVM_BE=$NVM_BE nvm_dev info $NVM_DEV_IDENT"; then
  test::fail
fi

test::pass
