# AAA tokenomics

[![GitHub Super-Linter](https://github.com/longtailfinancial/aaa-tokenomics/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

Modelling tokenomics similar to https://fantohm.com/ for our use case.

## AAA Model Diagrams

https://miro.com/app/board/uXjVOXwHq1M=/

## Reading Resources on OHM model

https://www.jordanmmck.com/crypto/olympus-dao?s=09

https://0xkowloon.substack.com/p/dissecting-the-olympus-protocol

https://forum.olympusdao.finance/d/77-oip-18-reward-rate-framework-and-reduction

# Deployment
To be able to install aaa-tokenomics as Python pakcage, you need to have ssh-key setup with Github and proper access rights to this repo.  

```
pip install git+ssh://git@github.com/longtailfinancial/aaa-tokenomics.git@danny#egg=aaa-tokenomics
```

## Requirements
Python >= 3.10  
[Virtualfish](https://virtualfish.readthedocs.io/en/latest/install.html)  
[Ssh-key on github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## Installation 
```
# Start new virtual fish environment (you can replace 'AAA' into something you prefer)
$ vf new AAA

# Activate the new environment
$ vf activate AAA

# Pip install AAA package 
# Note: requires ssh-key setup with your github account with access to this repo
$ python3 -m pip install git+ssh://git@github.com/longtailfinancial/aaa-tokenomics.git@main#egg=aaa
```
### Updating package
```
# Uninstall AAA package
$ vf activate AAA
$ python3 -m pip uninstall aaa

# Install updated package
$ python3 -m pip install git+ssh://git@github.com/longtailfinancial/aaa-tokenomics.git@main#egg=aaa
```

## Progress:
- [x] Setup this project as Python package to be pip installable
- [x] Implement visual presentation of the simulation
- [x] Add dynamic simulation state configuration (seats tiers, ticket price increase and purchase probability)
- [x] Bring back Github Actions with better code linter
- [x] Build the skeleton of the simulation (concert attendee and market)
=======
## Development
Update package requirements at pyproject.toml if you have installed or updated a
python package. 


## Warning

There is currently an issue with pip's format when doing "pip freeze".
Refer to this thread:

https://stackoverflow.com/questions/62885911/pip-freeze-creates-some-weird-path-instead-of-the-package-version

Solution is to simply use:
```
pip list --format=freeze > requirements.txt
```

instead of pip freeze.
