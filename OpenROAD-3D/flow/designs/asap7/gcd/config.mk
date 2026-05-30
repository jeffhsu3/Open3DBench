export DESIGN_NAME = gcd
export DESIGN_NICKNAME = gcd
export PLATFORM    = asap7

export VERILOG_FILES = ./designs/src/$(DESIGN_NICKNAME)/gcd.v
export SDC_FILE      = ./designs/asap7/gcd/gcd.sdc

export DIE_AREA    = 0 0 50 50
export CORE_AREA   = 2.16 2.16 47.52 47.52

export PLACE_DENSITY = 0.40
export DETAILED_ROUTE_ARGS = -droute_end_iter 1
export GLOBAL_ROUTE_ARGS = -allow_congestion -verbose -congestion_iterations 1
