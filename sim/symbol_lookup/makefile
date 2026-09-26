TOPDIR := $(abspath $(CURDIR)/../..)

SIM = verilator
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(TOPDIR)/rtl/symbol_lookup.sv $(TOPDIR)/rtl/crc32.sv
TOPLEVEL = symbol_lookup
COCOTB_TEST_MODULES = test_symbol_lookup

export PYTHONPATH := $(TOPDIR)/tb

include $(shell cocotb-config --makefiles)/Makefile.sim

# symbol_table.mem is generated, not committed. Build it if it is missing or if
# the generator or the symbol list changed. This block must sit AFTER the
# include, otherwise it becomes the default goal and the sim never runs.
$(TOPDIR)/tools/symbol_table.mem: $(TOPDIR)/tools/symbol_table.py $(TOPDIR)/tools/top1000.txt
	cd $(TOPDIR)/tools && python3 symbol_table.py

sim: $(TOPDIR)/tools/symbol_table.mem
