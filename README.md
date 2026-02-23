# Arelle Test Engine

[![Arelle Banner](https://arelle.org/arelle/wp-content/themes/platform/images/logo-platform.png)](https://arelle.org/)

## Description

A test engine for [Arelle](https://github.com/Arelle/Arelle).

Improves on Arelle's internal test suite validation process:
- Optional multiprocessing.
- Each testcase is an independent execution of Arelle via the Session API.
- Each execution is representative of the true behavior of Arelle (no test-specific pathways or logic).
- Each execution is easily reproducible (each execution produces runtime options JSON that can be used with `--optionsFile`).
- Each execution produces a dedicated log file.

## Installing the Test Engine

### Standalone Installation {#standalone-installation}
To use the Arelle Test Engine separately from a local copy of the Arelle source code,
clone this repository and install dependencies:
```bash
pip install -r requirements.txt
```
This will install a recent version of Arelle (and the necessary dependencies) to run the test engine against.

### Installation within an Arelle Development Environment
The Arelle Test Engine will eventually be incorporated into Arelle as a top-level module within the Arelle repository.
To simulate this setup, you can symlink the `arelle_test_engine` directory into your Arelle development environment.
From the root of your Arelle development environment, run:
```bash
ln -s /path/to/arelle-test-engine/arelle_test_engine arelle_test_engine
```
Alternatively, copying the directory will also work.

## Using the Test Engine

### Use as a Command Line Tool
```
python -m arelle_test_engine --help
usage: python -m arelle_test_engine [-h] [--config CONFIG] [--compare-formula-output] [--filter FILTERS] [--ignore-level {ok,satisfied,not_satisfied,warning,error}] [--log-directory LOG_DIRECTORY] [--match {all,any}] [--name NAME] [--parallel] [--series] [--processes PROCESSES] [--report REPORTS] [index_file]

Arelle Test Engine

positional arguments:
  index_file            Path to the test index file (optional if provided in config).

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to a JSON configuration file.
  --compare-formula-output
                        Treat 'instance' elements in expected testcase results as expected formula output rather than instance facts.
  --filter FILTERS      If any are provided, only testcases with an ID matching a filter will be executed.
  --ignore-level {ok,satisfied,not_satisfied,warning,error}
                        Errors with the specified level(s) will be ignored when evaluating testcase results.
  --log-directory LOG_DIRECTORY
                        If provided, test logs will be written to files in this directory. Otherwise logs will be written to standard output.
  --match {all,any}     Whether all constraints must be met for a testcase to pass (match-all), or if any single constraint being met is sufficient (match-any).
  --name NAME           An optional name for this test run, used in logging and reporting.
  --parallel            Whether to execute testcases in parallel (series execution is the default).
  --series              Whether to execute testcases in series.
  --processes PROCESSES
                        The number of worker processes to use for parallel execution. If not provided, the number of available CPU cores will be used.
  --report REPORTS      Generate report(s) in the following formats: CSV, HTML, JSON, XLSX, XML.
```

The Arelle Test Engine can be uses as a command line tool by passing options by:
- Command line arguments: 
  - `python -m arelle_test_engine "path/to/index.xml" --parallel`
- A configuration file: 
  - `python -m arelle_test_engine --config "path/to/config.json"`
- A combination of both (command line arguments will override config file options): 
  - `python -m arelle_test_engine "path/to/index.xml" --config "path/to/config.json" --parallel`

Certain options (those involving more complex data structures) can only be configured by file.
See [`TestEngineOptions`](./arelle_test_engine/test_engine_options.py) for more details on available options and their formats.

### Using as a Python Module
```python
from arelle_test_engine.test_engine import TestEngine
from arelle_test_engine.test_engine_options import TestEngineOptions

options = TestEngineOptions(...)
test_engine = TestEngine(options)
result = test_engine.run()
if any(
        not r.passed and not r.skip
        for r in result.testcase_results
):
    print("FAIL")
else:
    print("PASS")
```


## Testing the Test Engine
Note: A [standalone installation](#standalone-installation) is required to run the tests for the Arelle Test Engine.

### Run Unit Tests
```bash
pytest tests/unit_tests
```

### Run Integration Tests
The integration test runner is a wrapper for the test engine.
```
python -m tests.integration_tests.validation.run_conformance_suites --help
options:
  -h, --help            show this help message and exit
  --all                 Select all configured conformance suites
  --build-cache         Use CacheBuilder plugin to build cache from conformance suite usage
  --download-cache      Download and apply pre-built cache package and taxonomy packages
  --download-overwrite  Download (and overwrite) selected conformance suite files
  --download-missing    Download missing selected conformance suite files
  --download-private    Download privately hosted assets (AWS CLI and environment variables required)
  --list                List names of all configured conformance suites
  --log-to-file         Writes logs and results to .txt and .csv files
  --name NAME           Select only conformance suites with given names, comma delimited
  --offline             Run without loading anything from the internet (local files and cache only)
  --public              Select all public conformance suites
  --series              Run shards in series
  --shard SHARD         comma separated list of 0-indexed shards to run
  --shard-count SHARD_COUNT
                        number of shards to split suite into
  --test                Run selected conformance suite tests
  --testcase-filter TESTCASE_FILTER
                        Filter test cases (see --testcaseFilter)
```

To run integration tests through pytest:
```bash
pytest tests/integration_tests/validation/test_conformance_suites.py --offline --log-to-file --download-missing --name=xbrl_dimensions_1_0 
```

## Documentation / Support / Contributing

Check out the README in the [Arelle repository](https://github.com/Arelle/Arelle) for more information.

## License

[Apache License 2.0][license]

[license]: https://arelle.readthedocs.io/en/latest/license.html
