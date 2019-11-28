#!/bin/bash
set -e

# Load the environment
if [[ -n $CONDA ]]; then
    . $CONDA/etc/profile.d/conda.sh
    conda activate vplot
fi

# Install dependencies
conda install -y -q -c conda-forge pandoc
conda install -y -q ipykernel
conda update -y -q nb_conda nb_conda_kernels nb_anacondacloud
pip install -U sphinx
pip install -U "nbconvert>=5.5"
pip install -U sphinx_rtd_theme
pip install -U nbsphinx
pip install -U jupyter_client

# List available kernels
jupyter kernelspec list

# Build the docs
make -C docs html

# Copy the coverage over
cp -r coverage docs/_build/html/

# Force push if not pull request
if [[ -n $BUILDREASON ]] && [[ $BUILDREASON != "PullRequest" ]]; then

    cd docs/_build/html
    git init
    touch .nojekyll
    git add .nojekyll
    git add -f *
    git -c user.name='rodluger' -c user.email='rodluger@gmail.com' \
        commit -m "rebuild gh-pages"
    git push -f https://$GHUSER:$GHKEY@github.com/VirtualPlanetaryLaboratory/vplot \
        HEAD:gh-pages >/dev/null 2>&1 -q

fi