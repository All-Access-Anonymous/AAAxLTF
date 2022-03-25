# AAA tokenomics

Modelling tokenomics similar to Olympous DAO.

[AAA Model Diagrams in Miro](https://miro.com/app/board/uXjVOXwHq1M=/)

## Resources on OHM model:
https://olympusdaonow.com/ohm-token-defi-2-0-platform-liquidity-v33-explained-march-22-examples-list-of-olympus-dao-forks-mkr-crv-time/

https://www.jordanmmck.com/crypto/olympus-dao?s=09

https://0xkowloon.substack.com/p/dissecting-the-olympus-protocol

https://forum.olympusdao.finance/d/77-oip-18-reward-rate-framework-and-reduction

---

# Deployment
To be able to install aaa-tokenomics defi model as Python pakcage, you need to have ssh-key setup with Github and proper access rights to this repo.  

```
pip install git+ssh://git@github.com/longtailfinancial/aaa-tokenomics.git@defi-model#egg=aaa-defi
```

## Requirements
Python >= 3.8
[Virtualfish](https://virtualfish.readthedocs.io/en/latest/install.html)  
[Ssh-key on github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## Installation 
```
# Start new virtual fish environment (you can replace 'AAA' into something you prefer)
$ vf new AAA

# Activate the new environment
$ vf activate AAA

# Pip install AAA Defi package 
# Note: requires ssh-key setup with your github account with access to this repo
$ pip install git+ssh://git@github.com/longtailfinancial/aaa-tokenomics.git@defi-model#egg=aaa-defi
```
## Usage
```
from defi.sim_handler import SimHandler
from defi.config import sim_conf

s = SimHandler(sim_conf)
df, dfa, f = s.run()

print(df)
```


### Updating package
```
# Uninstall AAA package
$ vf activate AAA
$ pip uninstall aaa

# Install updated package
$ pip install git+ssh://git@github.com/longtailfinancial/aaa-tokenomics.git@defi-model#egg=aaa-defi
```
---

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
