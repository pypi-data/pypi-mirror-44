#!/bin/bash
this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHON_EXECUTABLE=/Users/travis/.pyenv/versions/2.7.14/bin/python
export PYTHON_PATH=${this_dir}:/Users/travis/build/sci-visus/OpenVisus/build/RelWithDebInfo/site-packages/OpenVisus:/Users/travis/.pyenv/versions/2.7.14/lib/python27.zip:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/plat-darwin:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/plat-mac:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/plat-mac/lib-scriptpackages:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/lib-tk:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/lib-old:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/lib-dynload:/Users/travis/.pyenv/versions/2.7.14/lib/python2.7/site-packages
export DYLD_LIBRARY_PATH=/Users/travis/.pyenv/versions/2.7.14/lib
if [ -d ${this_dir}/bin/Qt ]; then 
   echo "Using internal Qt5
   export Qt5_DIR=${this_dir}/bin/Qt
else
   echo "Using external PyQt5
   export Qt5_DIR=$(${PYTHON_EXECUTABLE} -c "import os,PyQt5; print(os.path.dirname(PyQt5.__file__))")
fi
export QT_PLUGIN_PATH=${Qt5_DIR}/plugins
cd ${this_dir}
${this_dir}/bin/visusviewer.app/Contents/MacOS/visusviewer $@
