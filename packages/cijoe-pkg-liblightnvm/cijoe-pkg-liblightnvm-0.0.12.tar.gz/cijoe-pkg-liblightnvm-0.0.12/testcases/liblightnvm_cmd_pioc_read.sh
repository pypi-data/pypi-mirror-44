#!/bin/bash
#
# Verify liblightnvm IO command pass-through via `nvm_cmd ptio`
#
# Passes through a read command without a payload
#
# shellcheck disable=SC2119
#
CIJ_TEST_NAME=$(basename "${BASH_SOURCE[0]}")
export CIJ_TEST_NAME
# shellcheck source=modules/cijoe.sh
source "$CIJ_ROOT/modules/cijoe.sh"
test::enter

CMD_FNAME="liblightnvm_ptio_read.ncmd"
CMD_PATH="/tmp/${CMD_FNAME}"

if ! ssh::push "$CIJ_TESTFILES/${CMD_FNAME}" "$CMD_PATH"; then
  test::fail
fi

# Send the pass-through command
if ! ssh::cmd "NVM_BE=$NVM_BE nvm_cmd pioc $NVM_DEV_IDENT \
                                          -c $CMD_PATH"; then
  test::fail
fi

test::pass
