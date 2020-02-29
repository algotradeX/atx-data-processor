# atx-data-processor usage
Process data from atx-database




## Setup Instructions

### 1. Install Pip
### 2. Install Anaconda
##### Linux
`>> wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh`

`>> bash ./Miniconda3-latest-Linux-x86_64.sh`

##### MacOS
`>> brew cask install anaconda`

`>> export PATH="/usr/local/anaconda3/bin:$PATH"`

##### Clone atx-data-processor
`>> git clone https://github.com/algotradeX/atx-data-processor.git`

##### Run virtual env
`>> conda create -n atx-dp-env python=3.7`

```
To activate this environment, use
$ conda activate atx-dp-env
To deactivate an active environment, use
$ conda deactivate
```

`>> conda activate atx-dp-env`

##### Install Packages

`>> pip install -r requirements.txt`

##### Update package and versions in requirements.txt

`>> pip freeze > requirements.txt`




## Run application
`>> python atx_data_processor_master.py`

    started atx-data-processor mongo connector {}
    started atx-data-processor server {}
     * Serving Flask app "atxdataprocessor.server" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://0.0.0.0:8420/ (Press CTRL+C to quit)




