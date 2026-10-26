# Discontiguous DRAM description

`device_tree.preserve_memory_ranges = true` explicitly enables multiple hardware
DRAM banks. ADT exports exact little-endian pairs in `/memory/reg` and
`/chosen/dram-ranges`, and preserves DTS reserved-memory regions. Missing, empty,
overlapping and64-bit-overflowing ranges are rejected. Existing single-bank
output remains unchanged when the option is absent.

The scalar base and summed byte count are descriptive compatibility fields.
They do not create contiguous RAM, fill holes, grant ownership, or authorize
allocation. The loader must still obtain actual UEFI ownership for every loaded
range and account for reserved regions. `device_tree.export_arch_timer = true`
also exports the original architectural timer at `/timer` for diagnostic readers;
the CPU timebase still comes from the standard `/cpus` description.

Firmware preflight receives the resolved UNIXNU_FRAMEWORK, UNIXNU_DEVICE,
UNIXNU_UEFI, UNIXNU_EDK2, UNIXNU_BUILD_TREE and UNIXNU_BUILD_WORK paths. Board
staging can bind generated dependencies without guessing sibling checkout names.
