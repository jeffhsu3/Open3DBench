####################################
# global connections
####################################
add_global_connection -net {VDD} -inst_pattern {.*} -pin_pattern {^VDD$} -power
add_global_connection -net {VDD} -inst_pattern {.*} -pin_pattern {^VDDPE$}
add_global_connection -net {VDD} -inst_pattern {.*} -pin_pattern {^VDDCE$}
add_global_connection -net {VSS} -inst_pattern {.*} -pin_pattern {^VSS$} -ground
add_global_connection -net {VSS} -inst_pattern {.*} -pin_pattern {^VSSE$}
global_connect
####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
####################################
# standard cell grid (Bottom Die)
####################################
define_pdn_grid -name {bottom_grid} -voltage_domains {CORE} -pins {M6}
add_pdn_stripe -grid {bottom_grid} -layer {M1} -width {0.072} -pitch {2.16} -offset {0} -followpins
add_pdn_stripe -grid {bottom_grid} -layer {M2} -width {0.072} -pitch {2.16} -offset {0} -followpins
add_pdn_stripe -grid {bottom_grid} -layer {M5} -width {0.48} -spacing {0.288} -pitch {21.6} -offset {1.2}
add_pdn_stripe -grid {bottom_grid} -layer {M6} -width {1.152} -spacing {0.384} -pitch {21.6} -offset {2.052}
add_pdn_connect -grid {bottom_grid} -layers {M1 M2}
add_pdn_connect -grid {bottom_grid} -layers {M2 M5}
add_pdn_connect -grid {bottom_grid} -layers {M5 M6}

####################################
# standard cell grid (Top Die)
####################################
define_pdn_grid -name {top_grid} -voltage_domains {CORE} -pins {M13}
add_pdn_stripe -grid {top_grid} -layer {M18} -width {0.072} -pitch {2.16} -offset {0} -followpins
add_pdn_stripe -grid {top_grid} -layer {M17} -width {0.072} -pitch {2.16} -offset {0} -followpins
add_pdn_stripe -grid {top_grid} -layer {M14} -width {0.48} -spacing {0.288} -pitch {21.6} -offset {1.2}
add_pdn_stripe -grid {top_grid} -layer {M13} -width {1.152} -spacing {0.384} -pitch {21.6} -offset {2.052}
add_pdn_connect -grid {top_grid} -layers {M17 M18}
add_pdn_connect -grid {top_grid} -layers {M14 M17}
add_pdn_connect -grid {top_grid} -layers {M13 M14}

####################################
# macro grids
####################################
define_pdn_grid -name {CORE_macro_grid_1} -voltage_domains {CORE} -macro \
  -orient {R0 R180 MX MY} -halo {2.0 2.0 2.0 2.0} -default
add_pdn_connect -grid {CORE_macro_grid_1} -layers {M4 M5}
add_pdn_connect -grid {CORE_macro_grid_1} -layers {M14 M15}

define_pdn_grid -name {CORE_macro_grid_2} -voltage_domains {CORE} -macro \
  -orient {R90 R270 MXR90 MYR90} -halo {2.0 2.0 2.0 2.0} -default
add_pdn_connect -grid {CORE_macro_grid_2} -layers {M4 M5}
add_pdn_connect -grid {CORE_macro_grid_2} -layers {M14 M15}
