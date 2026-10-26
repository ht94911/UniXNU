# Discontiguous DRAM

Use this option when the hardware DTS describes separate DRAM banks:

```toml
[device_tree]
preserve_memory_ranges = true
```

The generator exports each address/length pair in `/memory/reg` and
`/chosen/dram-ranges`, preserving holes between banks. It also exports the DTS
reserved-memory ranges. Missing, empty, overlapping and overflowing ranges are
rejected. Existing single-bank output is unchanged when the option is absent.

`dram-base` and the summed `dram-size` are descriptive compatibility fields.
They do not describe a contiguous allocation. The loader must obtain current
UEFI ownership for every loaded range and exclude reserved memory.

`device_tree.export_arch_timer = true` exports the hardware architectural timer
at `/timer` for diagnostic consumers. CPU timebase properties still come from
the standard `/cpus` description.

Compile the board DTS and generate the ADT using the [device-tree procedure](device-tree).
Compare all bank and reservation boundaries before [firmware integration](uefi-firmware).
