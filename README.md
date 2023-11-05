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

# Style
Style is preserved by pre-commit action. 
It is hooked automatically at installation time.
However, to run it manually:
```
pre-commit run --all-files
```


## TODO

### chore
- add linters (black, flake8, pylint, mypy, isort)
- replace set/source/set with dotenv or something like that
- add version control shortcuts in visual code
- get envs from remote
- add dockerised dev env ( one shot dev creation )
 
### feat
- add test to work on a single file, single feature
- try parallel file scraping
