PWD=$(shell pwd)

export PYTHONPATH := $(PWD)/../model:$(PYTHONPATH)

VERILOG_SOURCES = $(PWD)/../hdl/round.v $(PWD)/../hdl/siphash.v

TOPLEVEL := siphash
MODULE   := test_siphash

include $(shell cocotb-config --makefiles)/Makefile.sim