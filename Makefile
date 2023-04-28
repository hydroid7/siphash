MODULES := siphash/tests

.PHONY: $(MODULES)

venv:
	virtualenv -p python3.10 pyenv && pip3 install -r requirements.txt

.PHONY: all
all: $(MODULES)

$(MODULES):
	@cd $@ && $(MAKE)

.PHONY: clean
clean:
	$(foreach TEST, $(MODULES), $(MAKE) -C $(TEST) clean;)

.PHONY: test
test:
	$(foreach TEST, $(MODULES), $(MAKE) -C $(TEST);)