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
# standard cell grid
####################################
define_pdn_grid -name {top} -voltage_domains {CORE} -pins {M6}
add_pdn_stripe -grid {top} -layer {M1} -width {0.072} -pitch {2.16} -offset {0} -followpins
add_pdn_stripe -grid {top} -layer {M2} -width {0.072} -pitch {2.16} -offset {0} -followpins
add_pdn_stripe -grid {top} -layer {M5} -width {0.48} -spacing {0.288} -pitch {21.6} -offset {1.2}
add_pdn_stripe -grid {top} -layer {M6} -width {1.152} -spacing {0.384} -pitch {21.6} -offset {2.052}
add_pdn_connect -grid {top} -layers {M1 M2}
add_pdn_connect -grid {top} -layers {M2 M5}
add_pdn_connect -grid {top} -layers {M5 M6}
####################################
# macro grids
####################################
define_pdn_grid -name {CORE_macro_grid_1} -voltage_domains {CORE} -macro \
  -orient {R0 R180 MX MY} -halo {2.0 2.0 2.0 2.0} -default
add_pdn_connect -grid {CORE_macro_grid_1} -layers {M4 M5}
define_pdn_grid -name {CORE_macro_grid_2} -voltage_domains {CORE} -macro \
  -orient {R90 R270 MXR90 MYR90} -halo {2.0 2.0 2.0 2.0} -default
add_pdn_connect -grid {CORE_macro_grid_2} -layers {M4 M5}
