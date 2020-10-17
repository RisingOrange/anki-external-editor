SRC = $(realpath src)
ROOT = $(realpath ./)
TESTS = $(realpath tests)
BUILD = $(realpath build)
DEV_REQUIREMENTS = requirements.txt

export VERSION := $(shell git describe|awk -F"[-.]" '                  \
	{print $$1 "." $$2 "." $$3 + $$4}' 2>/dev/null || echo 0.0.1)

.PHONY: help tests echo tdd


help:  ## Show this help.
	@echo "\033[1mUsage:\033[0m"
	@echo "  make [target]\n"
	@echo "\033[1mTargets:\033[0m"
	@awk -F ":.*?## " -v und="\033[2mundocumented\033[0m" '            \
		/^[A-z][^:\t ]+:/&&NF==2{                                      \
			printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 | "sort"    \
		}                                                              \
		/^[A-z][^:\t ]+:/&&NF==1{                                      \
			split($$1, a, ":");                                        \
			printf "  \033[36m%-12s\033[0m %s\n", a[1], und | "sort"   \
		}' $(MAKEFILE_LIST)


echo:  ## Shows environment variables
	@echo SRC=${SRC}
	@echo ROOT=${ROOT}
	@echo TESTS=${TESTS}
	@echo VERSION=${VERSION}


build: tests clean ## Creates dist-ready file
	@-mkdir -p build/${VERSION} 2>/dev/null
	cd $(SRC);\
		zip -r $(BUILD)/${VERSION}/external_editor.ankiaddon *


clean:  ## Deletes old artifacts
	@-rm -r $(SRC)/__pycache__


tests: deps  ## run tests with PyTest
	python -m pytest --doctest-modules $(TESTS)


tdd: deps  ## run tests on filesystem events
	PYTHONPATH=$(ROOT) ptw -c \
		--runner 'pytest --stepwise --disable-warnings -v tests'  \
		--ignore src/deps
		./


deps: .deps  ## install dependencies
.deps: $(DEV_REQUIREMENTS)
	pip install --upgrade -r $(DEV_REQUIREMENTS)
	@touch .deps
