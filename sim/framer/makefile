TOPDIR := $(abspath $(CURDIR)/../..)

SIM = verilator
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(TOPDIR)/rtl/framer.sv
TOPLEVEL = framer
COCOTB_TEST_MODULES = test_framer

export PYTHONPATH := $(TOPDIR)/tb

include $(shell cocotb-config --makefiles)/Makefile.sim