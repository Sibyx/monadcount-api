#!/bin/bash
poetry export -f requirements.txt --without-hashes --with docker > requirements.txt
