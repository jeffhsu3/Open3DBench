export PROCESS = 7

export TECH_LEF = $(PLATFORM_DIR)/asap7_tech.lef
export SC_LEF = $(PLATFORM_DIR)/asap7sc7p5t_27_R_4x_201211.lef

export LIB_FILES = $(PLATFORM_DIR)/asap7sc7p5t_INVBUF_RVT_TT_nldm_201020.lib \
                   $(PLATFORM_DIR)/asap7sc7p5t_SIMPLE_RVT_TT_nldm_201020.lib \
                   $(PLATFORM_DIR)/asap7sc7p5t_AO_RVT_TT_nldm_201020.lib \
                   $(PLATFORM_DIR)/asap7sc7p5t_OA_RVT_TT_nldm_201020.lib \
                   $(PLATFORM_DIR)/asap7sc7p5t_SEQ_RVT_TT_nldm_201020.lib

export DFF_LIB_FILE = $(PLATFORM_DIR)/asap7sc7p5t_SEQ_RVT_TT_nldm_201020.lib

export DONT_USE_SC_LIB = $(OBJECTS_DIR)/lib/merged.lib

export PDN_TCL ?= $(PLATFORM_DIR)/grid_strategy-M1-M2-M5-M6.tcl

export DONT_USE_CELLS = 

# Fill cells
export FILL_CELLS ?= FILLER_ASAP7_75t_R FILLERxp5_ASAP7_75t_R

# Tie cells
export TIEHI_CELL_AND_PORT = TIEHIx1_ASAP7_75t_R H
export TIELO_CELL_AND_PORT = TIELOx1_ASAP7_75t_R L
export MIN_BUF_CELL_AND_PORTS = BUFx2_ASAP7_75t_R A Y
export ABC_DRIVER_CELL = BUFx2_ASAP7_75t_R
export ABC_LOAD_IN_FF = 0.5

# Floorplan
export PLACE_SITE = asap7sc7p5t
export IO_PLACER_H = M4
export IO_PLACER_V = M5
export TAP_CELL_NAME = TAPCELL_ASAP7_75t_R

# Place
export PLACE_DENSITY ?= 0.30

# CTS
export CTS_BUF_CELL   ?= BUFx4_ASAP7_75t_R

# Route
export MIN_ROUTING_LAYER = M2
export MAX_ROUTING_LAYER = M9

# Place padding
export CELL_PAD_IN_SITES_GLOBAL_PLACEMENT ?= 0
export CELL_PAD_IN_SITES_DETAIL_PLACEMENT ?= 0

