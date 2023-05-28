PWD=$(shell pwd)

export PYTHONPATH := $(PWD)/../model:$(PYTHONPATH)

VERILOG_SOURCES = \
	$(PWD)/../hdl/sip_round.v \
	$(PWD)/../hdl/siphash.v \
	$(PWD)/../hdl/sip_half_round.v \
	$(PWD)/../hdl/counter.v

TOPLEVEL := siphash
MODULE   := test_siphash

include $(shell cocotb-config --makefiles)/Makefile.sim


lint:
	verilator --lint-only -Wall --top-module $(TOPLEVEL) $(VERILOG_SOURCES)