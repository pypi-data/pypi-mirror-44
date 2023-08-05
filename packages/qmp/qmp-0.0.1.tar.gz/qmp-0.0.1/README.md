QEMU Monitor Protocol client
----------------------------

QEMU Monitor Protocol (QMP) is a JSON-based protocol that allows applications to
communicate with a QEMU instance.

This project packages an exact copy of `python/qemu/qmp.py` from the QEMU source
tree.

For a brief introduction to QMP, see
<https://github.com/qemu/qemu/blob/master/docs/interop/qmp-intro.txt>.

For detailed information about the protocol, see
<https://github.com/qemu/qemu/blob/master/docs/interop/qmp-spec.txt>.

For the full list of commands supported by QMP see *qemu-qmp-ref* man page,
which is available at
<https://manpages.debian.org/unstable/qemu-system-common/qemu-qmp-ref.7.en.html>.
