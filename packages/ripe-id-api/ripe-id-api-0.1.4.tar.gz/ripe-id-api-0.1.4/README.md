# RIPE ID API

Simple Python API client for RIPE ID.

## Configuration

* `RIPEID_BASE_URL` (`str`) - The base URL that is going to be used for API connections (defaults to `https://id.platforme.com/api/`)
* `RIPEID_LOGIN_URL` (`str`) - The base URL that is going to be used for visual web interactions (defaults to `https://id.platforme.com/`)
* `RIPEID_ID` (`str`) - The identifier of the client making use of the RIPE ID (defaults to `None`)
* `RIPEID_SECRET` (`str`) - The secret token to be used for authentication (defaults to `None`)
* `RIPEID_REDIRECT_URL` (`str`) - The URL for the redirection operation after the interactive part of the workflow (defaults to `None`)

## License

RIPE ID API is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://travis-ci.org/ripe-tech/ripe-id-api.svg?branch=master)](https://travis-ci.org/ripe-tech/ripe-id-api)
[![Coverage Status](https://coveralls.io/repos/ripe-tech/ripe-id-api/badge.svg?branch=master)](https://coveralls.io/r/ripe-tech/ripe-id-api?branch=master)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
