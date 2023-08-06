#!/bin/bash
#
# Verify OCSSD 2.0 GLP-CI via `nvm_cmd rprt_all`
#
# And that the environment has defined NVM_DEV_IDENT identifying the device to
# use for testing
#
# shellcheck disable=SC2119
#
CIJ_TEST_NAME=$(basename "${BASH_SOURCE[0]}")
export CIJ_TEST_NAME
# shellcheck source=modules/cijoe.sh
source "$CIJ_ROOT/modules/cijoe.sh"
test::enter

if ! ssh::cmd "NVM_BE=$NVM_BE nvm_cmd rprt_all $NVM_DEV_IDENT"; then
  test::fail
fi

test::pass
