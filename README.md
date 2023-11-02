# tado-thermostat-consumer
Collect, aggregate and plot data from a Tado thermostat.

# Installation
```
conda create --name tado-thermostat-consumer python=3.10
conda activate tado-thermostat-consumer
pip install -r requirements.txt
```

# Configuration
Create a `.env` lik `.env.example` and fill it.
Then, copy in you `.zshrc`:
```
set -o allexport; 
source ~/PycharmProjects/tado-thermostat-consumer/.env;
set +o allexport
```


## TODO

### chore
- add linters (black, flake8, pylint, mypy, isort)
- add test to work on a single file
- replace set/source/set with dotenv or something like that
 
### feat
- gather heat command
- plot heater command
- try parallel file scraping
