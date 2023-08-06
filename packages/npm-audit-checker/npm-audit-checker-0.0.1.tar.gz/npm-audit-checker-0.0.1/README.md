# npm-audit-checker

## Overview

This tool checks the output from `npm audit --summary --json` or `yarn audit --summary --json` and then fails based on the severity provided.

If there are vulnerabilities reported on or above the threshold passed the tool will exit with a non zero error code, which can be used in CI to fail builds.

## Background / Motivation

The [npm audit](https://docs.npmjs.com/cli/audit) tool currently doesn't allow a way of defining which severity of vulnerabilities should be considered acceptable out of the various levels defined for [npm security advisories](https://www.npmjs.com/advisories) - namely `info | low | moderate | high | critical`.

You might not care about `info` or `low` but want to fail CI jobs if a `moderate` or above is found, which used to be possible with [nsp](https://github.com/nodesecurity/nsp) using the `--cvss-threshold` option.

## Usage

```
- pip install npm-audit-checker
- npm audit --summary --json | npm-audit-checker
```

## Options
```
usage: npm-audit-checker [-h] [-t {low,moderate,high,critical}] [-d] [-v]

npm audit checker CLI

optional arguments:
  -h, --help            show this help message and exit
  -t {low,moderate,high,critical}, --threshold {low,moderate,high,critical}
                        Severity to fail on or above
  -d, --debug           Enable debug output
  -v, --version         Show the installed version of npm-audit-checker
```
