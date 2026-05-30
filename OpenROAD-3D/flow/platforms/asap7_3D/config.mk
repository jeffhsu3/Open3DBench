export PROCESS = 7

export TECH_LEF = $(PLATFORM_DIR)/lef/asap7_3D.tech.lef
export SC_LEF = $(PLATFORM_DIR)/lef_bottom/asap7sc7p5t_27_R_4x_201211.bottom.lef

export LIB_FILES = $(ADDITIONAL_LIBS)

export DFF_LIB_FILE = $(PLATFORM_DIR)/lib_bottom/asap7sc7p5t_SEQ_RVT_TT_nldm_201020.bottom.lib

export DONT_USE_SC_LIB = $(OBJECTS_DIR)/lib/merged.lib

export PDN_TCL ?= $(PLATFORM_DIR)/grid_strategy-M1-M2-M5-M6.tcl

export DONT_USE_CELLS = 

# Fill cells (defaults to bottom die for cell insertion)
export FILL_CELLS ?= FILLER_ASAP7_75t_R_bottom FILLERxp5_ASAP7_75t_R_bottom

# Tie cells
export TIEHI_CELL_AND_PORT = TIEHIx1_ASAP7_75t_R_bottom H
export TIELO_CELL_AND_PORT = TIELOx1_ASAP7_75t_R_bottom L
export MIN_BUF_CELL_AND_PORTS = BUFx2_ASAP7_75t_R_bottom A Y
export ABC_DRIVER_CELL = BUFx2_ASAP7_75t_R_bottom
export ABC_LOAD_IN_FF = 0.5

# Floorplan
export PLACE_SITE = asap7sc7p5t
export IO_PLACER_H = M4
export IO_PLACER_V = M5
export TAP_CELL_NAME = TAPCELL_ASAP7_75t_R_bottom

# Place
export PLACE_DENSITY ?= 0.30

# CTS
export CTS_BUF_CELL   ?= BUFx4_ASAP7_75t_R_bottom

# Route (M1 to M9 are bottom, M10 to M18 are upper)
export MIN_ROUTING_LAYER = M2
export MAX_ROUTING_LAYER = M18

# Place padding
export CELL_PAD_IN_SITES_GLOBAL_PLACEMENT ?= 0
export CELL_PAD_IN_SITES_DETAIL_PLACEMENT ?= 0

