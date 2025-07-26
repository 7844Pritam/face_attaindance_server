#!/usr/bin/env bash

# Upgrade setuptools/pip/wheel to compatible versions before anything else
pip install --upgrade "setuptools>=69.0.0" "wheel>=0.40.0" "pip>=24.0"

# Now install your project dependencies
pip install -r requirements.txt

