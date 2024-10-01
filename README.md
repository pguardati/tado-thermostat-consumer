# tado-thermostat-consumer
Collect, aggregate and plot data from a Tado thermostat.

# Installation
```bash
conda create --name tado-thermostat-consumer python=3.10
conda activate tado-thermostat-consumer
pip install -r requirements.txt
```

# Configuration
Create a `.env` lik `.env.example` and fill it.
Then, copy in you `.zshrc`:
```bash
set -o allexport; 
source ~/PycharmProjects/tado-thermostat-consumer/.env;
set +o allexport
```

# Style
Style is preserved by pre-commit action. 
It is hooked automatically at installation time.
However, to run it manually:
```bash
pre-commit run --all-files
```

# Usage
```bash
python src/main.py --start_date 2023-05-18 --reload_today=True
```


## TODO

### chore
- add linters (black, flake8, pylint, mypy, isort)
- replace set/source/set with dotenv or something like that
- add version control shortcuts in visual code
- get envs from remote ( use go-based sops )
- add dockerised dev env ( one shot dev creation )
 
### feat
- add test to work on a single file, single feature
- try parallel file scraping
- add daily heater usage
