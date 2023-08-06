#!/bin/bash
this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHON_EXECUTABLE=/Users/travis/.pyenv/versions/3.6.5/bin/python
export PYTHON_PATH=${this_dir}:/Users/travis/build/sci-visus/OpenVisus/build/RelWithDebInfo/site-packages/OpenVisus:/Users/travis/.pyenv/versions/3.6.5/lib/python36.zip:/Users/travis/.pyenv/versions/3.6.5/lib/python3.6:/Users/travis/.pyenv/versions/3.6.5/lib/python3.6/lib-dynload:/Users/travis/.pyenv/versions/3.6.5/lib/python3.6/site-packages
export DYLD_LIBRARY_PATH=/Users/travis/.pyenv/versions/3.6.5/lib
${this_dir}/bin/visus.app/Contents/MacOS/visus $@
