#!/bin/bash
#
# Verify liblightnvm -- OCSSD 2.0 vector copy -- via `nvm_test_cmd_copy`
#
# This is a test-wrapper, wrapping the test provided by liblightnvm and thus
# assumes that liblightnvm is installed on the target system and that an
# Open-Channel SSD is available on the system and identified by the environment
# variable NVM_DEV_IDENT
#
# shellcheck disable=SC2119
#
CIJ_TEST_NAME=$(basename "${BASH_SOURCE[0]}")
export CIJ_TEST_NAME
# shellcheck source=modules/cijoe.sh
source "$CIJ_ROOT/modules/cijoe.sh"
test::enter

if ! ssh::cmd "NVM_BE=$NVM_BE nvm_test_cmd_copy $NVM_DEV_IDENT 0 0"; then
  test::fail
fi

test::pass
