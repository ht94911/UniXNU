# 多段DRAM描述

板级`device_tree.preserve_memory_ranges = true`显式启用多段内存描述。
ADT在`/memory/reg`和`/chosen/dram-ranges`保留实际小端地址/长度对，并导出
DTS保留内存；缺失、零长度、重叠和64位越界会拒绝。未启用时原单段输出不变。

基础地址与长度总和仅为兼容描述，不填补地址空洞、不授予内存所有权；loader仍须
实际取得UEFI分配并排除保留区。`device_tree.export_arch_timer = true`额外在
`/timer`保留原始架构定时器供诊断读取，CPU时基仍来自标准`/cpus`描述。

固件preflight显式获得解析后的框架、设备、UEFI、EDK2、tree和work目录环境，
用于在生成目录构建板级依赖，不能由缺少参数静默降级为无保护构建。
