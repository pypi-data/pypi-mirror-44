#!/usr/bin/env bash
#
# ZBLK
#
# nvme:
#
# Un-comment the line below and point it to the NVMe/OCSSD device to use
#
#export NVME_DEV_NAME=nvme0n1

# lightnvm:
: "${LNVM_DEV_TYPE:=zblk}";                     export LNVM_DEV_TYPE
: "${LNVM_BGN:=0}";                             export LNVM_BGN
: "${LNVM_END:=31}";                            export LNVM_END

: "${LNVM_DEV_NAME:=${NVME_DEV_NAME}b00${LNVM_BGN}e0${LNVM_END}}"; export LNVM_DEV_NAME
: "${LNVM_DEV_PATH:=/dev/$LNVM_DEV_NAME}";      export LNVM_DEV_PATH

# The ZBLK parallel unit range is managed by the variables "LNVM_BGN", and
# "LNVM_END". The ZBLK hook will, via the LNVM module, create and remove
# instances based on the variables defined above.

# block:
: "${BLOCK_DEV_NAME:=$LNVM_DEV_NAME}";          export BLOCK_DEV_NAME
: "${BLOCK_DEV_PATH:=$LNVM_DEV_PATH}";          export BLOCK_DEV_PATH

# Some of the test tools rely only on a block device, e.g. fio. The above
# exports the ZBLK instance as the block device for these tests.

# fs:
: "${FS_MOUNT_POINT:=/mnt/cijoe_fs_tests}";     export FS_MOUNT_POINT

# Other test tools e.g. xfstests, require a block device and a place to
# mount/umount/ wipe file-systems. FS_MOUNT defines this.
