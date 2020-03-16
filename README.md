# atx-data-processor
Process data from atx-database

![Python package](https://github.com/algotradeX/atx-data-processor/workflows/Python%20package/badge.svg?label=Build%20Status)
![codeclimate-maintainability](https://img.shields.io/codeclimate/maintainability/algotradeX/atx-data-processor?label=Code%20Climate%20Maintainability)


### Code Climate Status
![codeclimate-maintainability-percentage](https://img.shields.io/codeclimate/maintainability-percentage/algotradeX/atx-data-processor?style=plastic)
![codeclimate-issue-count](https://img.shields.io/codeclimate/issues/algotradeX/atx-data-processor?style=plastic)
![codeclimate-tech-debt](https://img.shields.io/codeclimate/tech-debt/algotradeX/atx-data-processor?style=plastic)
![codeclimate-coverage](https://img.shields.io/codeclimate/coverage/algotradeX/atx-data-processor?style=plastic)


## Setup Instructions

### 1. Install Pip
### 2. Install Anaconda
##### Linux
`wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh`

`bash ./Miniconda3-latest-Linux-x86_64.sh`

##### MacOS
`brew cask install anaconda`

`export PATH="/usr/local/anaconda3/bin:$PATH"`

##### Clone atx-data-processor
`git clone https://github.com/algotradeX/atx-data-processor.git`

##### Run virtual env
`conda create -n atx-dp-env python=3.7`

```
To activate this environment, use
$ conda activate atx-dp-env
To deactivate an active environment, use
$ conda deactivate
```

`conda activate atx-dp-env`

##### Install Packages

`pip install -r requirements.txt`

##### Update package and versions in requirements.txt

`pip freeze > requirements.txt`




## Run application
`python atx_data_processor_master.py`

    started atx-data-processor mongo connector {}
    started atx-data-processor server {}
     * Serving Flask app "atxdataprocessor.server" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://0.0.0.0:8420/ (Press CTRL+C to quit)



## Linting and Formatter

#### Formatting using black

`black src/ atx_data_processor_master.py`

#### Linting using flake8

`flake8 src/ atx_data_processor_master.py`

#### Install the hooks

Install the git hooks defined in the pre-commit file by running the following in the terminal:

`pre-commit install`

#### Run the hooks

If this is an already existing project you may want to go ahead and format all the files. You can do this by running the following in the terminal:

`pre-commit run --all-files`

This will run all the git hooks you've installed against all files. At this point you can review the messages and make corrections as necessary. You can re-run the command until there are no longer any warnings.

Finally, commit all the new changes! From now on when you stage files to be committed only those will be formatted and linted by black and flake8. 



