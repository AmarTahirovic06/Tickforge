MODULES = counter shift_reg framer

.PHONY: all clean $(MODULES)

all: $(MODULES)

$(MODULES):
	@echo "===== $@ ====="
	@$(MAKE) -C sim/$@

clean:
	@rm -rf sim/*/sim_build sim/*/results.xml