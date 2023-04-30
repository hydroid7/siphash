MODULES := siphash/tests

EXTRA_ARGS += --coverage

.PHONY: $(MODULES)

venv:
	virtualenv -p python3.10 pyenv && pip3 install -r requirements.txt

.PHONY: all
all: $(MODULES)

$(MODULES):
	@cd $@ && $(MAKE)

.PHONY: clean
clean:
	$(foreach MOD, $(MODULES), $(MAKE) -C $(MOD) clean;)

.PHONY: test
test:
	$(foreach MOD, $(MODULES), $(MAKE) -C $(MOD);)

regression:
	$(foreach MOD, $(MODULES), $(MAKE) -C $(MOD) regression;)

lint:
	$(foreach MOD, $(MODULES), $(MAKE) -C $(MOD) lint;)