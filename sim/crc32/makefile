TOPDIR := $(abspath $(CURDIR)/../..)

SIM = verilator
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(TOPDIR)/rtl/crc32.sv
TOPLEVEL = crc32
COCOTB_TEST_MODULES = test_crc32

export PYTHONPATH := $(TOPDIR)/tb

include $(shell cocotb-config --makefiles)/Makefile.sim