# Bottom routing layers (M1 to M9)
set_layer_rc -layer M1 -resistance 7.04175E-02 -capacitance 1e-10
set_layer_rc -layer M2 -resistance 2.97126E-02 -capacitance 1.84542E-01
set_layer_rc -layer M3 -resistance 3.12872E-02 -capacitance 1.53955E-01
set_layer_rc -layer M4 -resistance 1.80365E-02 -capacitance 1.89434E-01
set_layer_rc -layer M5 -resistance 1.89936E-02 -capacitance 1.71593E-01
set_layer_rc -layer M6 -resistance 1.18797E-02 -capacitance 1.76146E-01
set_layer_rc -layer M7 -resistance 1.25097E-02 -capacitance 1.47030E-01
set_layer_rc -layer M8 -resistance 1.25097E-02 -capacitance 1.47030E-01
set_layer_rc -layer M9 -resistance 1.25097E-02 -capacitance 1.47030E-01

# Top routing layers (M10 to M18, symmetric to bottom)
set_layer_rc -layer M10 -resistance 1.25097E-02 -capacitance 1.47030E-01
set_layer_rc -layer M11 -resistance 1.25097E-02 -capacitance 1.47030E-01
set_layer_rc -layer M12 -resistance 1.25097E-02 -capacitance 1.47030E-01
set_layer_rc -layer M13 -resistance 1.18797E-02 -capacitance 1.76146E-01
set_layer_rc -layer M14 -resistance 1.89936E-02 -capacitance 1.71593E-01
set_layer_rc -layer M15 -resistance 1.80365E-02 -capacitance 1.89434E-01
set_layer_rc -layer M16 -resistance 3.12872E-02 -capacitance 1.53955E-01
set_layer_rc -layer M17 -resistance 2.97126E-02 -capacitance 1.84542E-01
set_layer_rc -layer M18 -resistance 7.04175E-02 -capacitance 1e-10

set_wire_rc -signal -resistance 3.23151E-02 -capacitance 1.73323E-01
set_wire_rc -clock -resistance 5.13971E-02 -capacitance 1.44549E-01

# Bottom via layers (V1 to V8)
set_layer_rc -via V1 -resistance 1.72E-02
set_layer_rc -via V2 -resistance 1.72E-02
set_layer_rc -via V3 -resistance 1.72E-02
set_layer_rc -via V4 -resistance 1.18E-02
set_layer_rc -via V5 -resistance 1.18E-02
set_layer_rc -via V6 -resistance 8.20E-03
set_layer_rc -via V7 -resistance 8.20E-03
set_layer_rc -via V8 -resistance 6.30E-03

# Hybrid bond via layer
set_layer_rc -via hb_layer -resistance 1.0E-02

# Top via layers (V10 to V17, symmetric to bottom)
set_layer_rc -via V10 -resistance 6.30E-03
set_layer_rc -via V11 -resistance 8.20E-03
set_layer_rc -via V12 -resistance 8.20E-03
set_layer_rc -via V13 -resistance 1.18E-02
set_layer_rc -via V14 -resistance 1.18E-02
set_layer_rc -via V15 -resistance 1.72E-02
set_layer_rc -via V16 -resistance 1.72E-02
set_layer_rc -via V17 -resistance 1.72E-02
