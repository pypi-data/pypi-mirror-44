#!/usr/bin/env bash
#
# liblightnvm
#
# The testcases explicitly forward the environment variable 'NVM_BE', the
# following section assigns 'NVM_DEV_IDENT' based on the value of 'NVM_BE'.
#
# NOTE:
# - Change the memory assigned to SPDK via env. var. 'HUGEMEM' in testplan
#

# liblightnvm; set NVM_DEV_IDENT
case $NVM_BE in
NVM_BE_IOCTL)
  : "${NVM_DEV_IDENT:=/dev/$NVME_DEV_NAME}"
  export NVM_DEV_IDENT
  ;;
NVM_BE_LBD)
  : "${NVM_DEV_IDENT:=/dev/$NVME_DEV_NAME}"
  export NVM_DEV_IDENT
  ;;
NVM_BE_SPDK)
  : "${NVM_DEV_IDENT:="traddr:$PCI_DEV_NAME"}"
  export NVM_DEV_IDENT
  ;;
NVM_BE_NOCD)
  : "${NVM_DEV_IDENT:="traddr:$PCI_DEV_NAME"}"
  export NVM_DEV_IDENT
  ;;
esac

