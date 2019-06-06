# quant_playground
This is a playground for trying out quant strategies with most of the common libraries installed.

## API Usage

#### pysnowball

Acquire your token by fowlloing the [instructions](https://blog.crackcreed.com/diy-xue-qiu-app-shu-ju-api/).

Please refer to [pysnowball](https://github.com/scli-James/pysnowball) for documentation.

#### Tushare.pro

Acquire your token at [link](https://tushare.pro/user/token).

Please refer to [tushare.pro](https://tushare.pro/document/2) for documentation.


## Environment

It is recommended that you run this repository in a conda environment. If you do not have miniconda or Anaconda pre-installed, please [download](https://docs.conda.io/en/latest/miniconda.html) conda and follow the [instructions](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) for installation.


#### Installation

`conda env create -f environment.yml`

#### Update

`conda env update -f environment.yml`

#### Activate/Deactivate

`conda activate quant`

`conda deactivate`


## Docs and Docs Generation

Please write [numpy style docstrings](https://numpydoc.readthedocs.io/en/latest/format.html) in your code. Refer to `utils.extract_sift_features` for example.

#### Linux or Mac OS

- Create or update docs: `make`
- Delete docs: `make clean`

#### Windows

- Create or update docs: `make.bat`
- Delete docs: `make.bat clean`


## Github helper scripts

#### Merge `master` to local branch

Make sure you are in your branch with `git checkouth BRANCH`

`sh github_helper/fast_forward.sh`

#### Create pull request after commit and push

With custom title and comment:

`sh github_helper/pull_request.sh "TITLE" ["COMMENT"]`

Without custom title and comment:

`sh github_helper/pull_request.sh --no-edit`


