#!/bin/sh
set -e

#check to see if miniconda folder is empty
if [ ! -d "$HOME/miniconda/miniconda/envs/test-environment" ]; then
  wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
  chmod +x miniconda.sh
  ./miniconda.sh -b -p $HOME/miniconda/miniconda
  export PATH="$HOME/miniconda/miniconda/bin:$PATH"
  conda config --set always_yes yes --set changeps1 no
  conda update -q conda
  conda info -a
  conda create -q -n test-environment python=$TRAVIS_PYTHON_VERSION pytest setuptools
  source activate test-environment
  which python
  pip install -q coveralls coverage
else
  echo "Miniconda already installed."
fi

if [ ! -f $HOME/downloads/praat.tar.gz ]; then
  mkdir -p $HOME/downloads
  curl -L -o $HOME/downloads/praat.tar.gz http://www.fon.hum.uva.nl/praat/praat5408_linux64.tar.gz;
  cd $HOME/downloads
  tar -zxvf praat.tar.gz --keep-newer-files
fi
