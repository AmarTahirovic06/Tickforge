TOPDIR := $(abspath $(CURDIR)/../..)

SIM = verilator
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(TOPDIR)/rtl/shift_reg.sv
TOPLEVEL = shift_reg
COCOTB_TEST_MODULES = test_shift_reg

export PYTHONPATH := $(TOPDIR)/tb

include $(shell cocotb-config --makefiles)/Makefile.sim