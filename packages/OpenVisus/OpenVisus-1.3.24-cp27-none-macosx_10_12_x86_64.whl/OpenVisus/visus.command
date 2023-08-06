#!/bin/bash
this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHON_EXECUTABLE=/Users/travis/.pyenv/versions/2.7.14/bin/python
export PYTHON_PATH=${this_dir}:/Users/travis/build/sci-visus/OpenVisus/build/RelWithDebInfo/site-packages/OpenVisus:/Users/travis/.pyenv/versions/2.7.14/lib/python27.zip:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/plat-darwin:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/plat-mac:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/plat-mac/lib-scriptpackages:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/lib-tk:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/lib-old:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/lib-dynload:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/site-packages
export DYLD_LIBRARY_PATH=/Users/travis/.pyenv/versions/2.7.14/lib
${this_dir}/bin/visus.app/Contents/MacOS/visus $@
