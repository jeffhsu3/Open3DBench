export DESIGN_NAME = gcd
export DESIGN_NICKNAME = gcd
export PLATFORM    = asap7_3D
export FLOW_VARIANT ?= 3D

export VERILOG_FILES = ./designs/src/$(DESIGN_NICKNAME)/gcd.v
export SDC_FILE      = ./designs/asap7_3D/gcd/gcd.sdc

export ADDITIONAL_LEFS = $(PLATFORM_DIR)/lef_upper/asap7sc7p5t_27_R_4x_201211.upper.lef

export ADDITIONAL_LIBS = $(PLATFORM_DIR)/lib_bottom/asap7sc7p5t_INVBUF_RVT_TT_nldm_201020.bottom.lib \
                         $(PLATFORM_DIR)/lib_bottom/asap7sc7p5t_SIMPLE_RVT_TT_nldm_201020.bottom.lib \
                         $(PLATFORM_DIR)/lib_bottom/asap7sc7p5t_AO_RVT_TT_nldm_201020.bottom.lib \
                         $(PLATFORM_DIR)/lib_bottom/asap7sc7p5t_OA_RVT_TT_nldm_201020.bottom.lib \
                         $(PLATFORM_DIR)/lib_bottom/asap7sc7p5t_SEQ_RVT_TT_nldm_201020.bottom.lib \
                         $(PLATFORM_DIR)/lib_upper/asap7sc7p5t_INVBUF_RVT_TT_nldm_201020.upper.lib \
                         $(PLATFORM_DIR)/lib_upper/asap7sc7p5t_SIMPLE_RVT_TT_nldm_201020.upper.lib \
                         $(PLATFORM_DIR)/lib_upper/asap7sc7p5t_AO_RVT_TT_nldm_201020.upper.lib \
                         $(PLATFORM_DIR)/lib_upper/asap7sc7p5t_OA_RVT_TT_nldm_201020.upper.lib \
                         $(PLATFORM_DIR)/lib_upper/asap7sc7p5t_SEQ_RVT_TT_nldm_201020.upper.lib

export DIE_AREA    = 0 0 50 50
export CORE_AREA   = 2.16 2.16 47.52 47.52

export PLACE_DENSITY = 0.40
export DETAILED_ROUTE_ARGS = -droute_end_iter 1
export GLOBAL_ROUTE_ARGS = -allow_congestion -verbose -congestion_iterations 1
