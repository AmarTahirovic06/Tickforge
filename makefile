MODULES = counter shift_reg framer crc32 symbol_lookup

VERILATOR_LINT = verilator --lint-only -Wall

.PHONY: all clean lint $(MODULES)

all: $(MODULES)

$(MODULES):
	@echo "===== $@ ====="
	@$(MAKE) -C sim/$@

lint:
	$(VERILATOR_LINT) rtl/counter.sv                     --top-module counter
	$(VERILATOR_LINT) rtl/shift_reg.sv                   --top-module shift_reg
	$(VERILATOR_LINT) rtl/framer.sv rtl/shift_reg.sv     --top-module framer
	$(VERILATOR_LINT) rtl/crc32.sv                       --top-module crc32
	$(VERILATOR_LINT) rtl/symbol_lookup.sv rtl/crc32.sv  --top-module symbol_lookup

clean:
	@rm -rf sim/*/sim_build sim/*/results.xml
