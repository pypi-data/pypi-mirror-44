#!/bin/bash
#
# Verify liblightnvm IO command pass-through via `nvm_cmd ptio`
#
# Passes through a read command with a 4K data payload
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

# Create data
if ! CMD_DATA_PATH=$(ssh::cmd_output "tempfile -d /tmp -s $CMD_FNAME.data"); then
  test::fail
fi
if ! ssh::cmd "dd if=/dev/zero of=$CMD_DATA_PATH bs=4096 count=1"; then
  test::fail
fi

# Send the pass-through command
if ! ssh::cmd "NVM_BE=$NVM_BE nvm_cmd pioc $NVM_DEV_IDENT \
                                          -c $CMD_PATH \
                                          -d $CMD_DATA_PATH"; then
  test::fail
fi

test::pass
