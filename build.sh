#!/bin/bash

set -e

rm -rf build && mkdir build && cd build && cmake .. && make -j8 && make host
