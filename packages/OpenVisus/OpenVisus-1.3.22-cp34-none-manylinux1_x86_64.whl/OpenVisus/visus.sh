#!/bin/bash
this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHON_EXECUTABLE=/root/.pyenv/versions/3.4.1/bin/python
export PYTHON_PATH=${this_dir}:/home/travis/build/sci-visus/OpenVisus/build/site-packages/OpenVisus:/root/.pyenv/versions/3.4.1/lib/python34.zip:/root/.pyenv/versions/3.4.1/lib/python3.4:/root/.pyenv/versions/3.4.1/lib/python3.4/plat-linux:/root/.pyenv/versions/3.4.1/lib/python3.4/lib-dynload:/root/.pyenv/versions/3.4.1/lib/python3.4/site-packages
export LD_LIBRARY_PATH=/root/.pyenv/versions/3.4.1/lib
${this_dir}/bin/visus $@
