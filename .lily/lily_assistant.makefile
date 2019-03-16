
#
# RENDERED FOR VERSION: 1.0.0
#
# WARNING: This file is autogenerated by the `lily_assistant` and any manual
# changes you will apply here will be overwritten by next
# `lily_assistant init <project>` invocation.
#

help:  ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

SHELL := /bin/bash

VERSION := $(shell python setup.py --version)

CHROME_EXISTS := $(shell command -v google-chrome)

TEST_COVERAGE_THRESHOLD := 90

#
# TEST LIFECYCLE TARGETS
#
# NOTE: Currently those targets are only here as place-holders for
# overwrites which will be run pre and post various test targets. See below.
#
.PHONY: test_setup
test_setup:
	printf "\n>> TEST SET UP\n"

.PHONY: test_teardown
test_teardown:
	printf "\n>> TEST TEAR DOWN\n"

.PHONY: assert_test_setup_was_run
assert_test_setup_was_run:
	printf "\n>> CHECK IF IN TEST SET UP WAS EXECUTED\n"

#
# LINTER & CODE QUALITY
#
.PHONY: lint
lint:  ## lint the lily_assistant & tests
	printf "\n>> [CHECKER] check if code fulfills quality criteria\n" && \
	source env.sh && \
	flake8 --ignore D100,D101,D102,D103,D104,D105,D106,D107,D202,D204,W504 tests && \
	flake8 --ignore D100,D101,D102,D103,D104,D105,D106,D107,D202,D204,W504 lily_assistant


#
# RUN TEST BOTH TYPES: UNIT + INTEGRATION
# should be used for complete test running
#

# -- TEST SELECTED
.PHONY: lily_assistant_test
lily_assistant_test:
	printf "\n>> [CHECKER] check if chosen tests are passing\n" && \
	source env.sh && \
	py.test --cov=lily_assistant --cov-fail-under=${TEST_COVERAGE_THRESHOLD} -r w -s -vv $(tests)

.PHONY: test
test: assert_test_setup_was_run lily_assistant_test  ## run selected tests

# -- TEST ALL
.PHONY: lily_assistant_test_all
lily_assistant_test_all:
	printf "\n>> [CHECKER] check if all tests are passing\n" && \
	source env.sh && \
	py.test --cov=lily_assistant --cov-fail-under=${TEST_COVERAGE_THRESHOLD} -r w -s -vv tests && \
    coverage html -d coverage_html

.PHONY: test_all
test_all: test_setup lily_assistant_test_all test_teardown  ## run all available tests


#
# COVERAGE
#
.PHONY: inspect_coverage
inspect_coverage: test_all  ## render html coverage report and jump to it
	if [ ! -z ${CHROME_EXISTS} ]; \
	then google-chrome coverage_html/index.html; \
	else open coverage_html/index.html; \
	fi
