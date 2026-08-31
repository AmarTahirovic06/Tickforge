TOPDIR := $(abspath $(CURDIR)/../..)

SIM = verilator
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(TOPDIR)/rtl/counter.sv
TOPLEVEL = counter
COCOTB_TEST_MODULES = test_counter

export PYTHONPATH := $(TOPDIR)/tb

include $(shell cocotb-config --makefiles)/Makefile.sim