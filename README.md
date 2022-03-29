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
$ vf new Mazzy

# Activate the new environment
$ vf activate Mazzy

# Pip install aaa-defi Defi package 
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
# Uninstall aaa-defi package
$ vf activate mazzy
$ pip uninstall aaa-defi

# Install updated package
$ python3 -m pip install git+ssh://git@github.com/longtailfinancial/aaa-tokenomics.git@defi-model#egg=aaa-defi
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

---
---

# Simulation

> The AAA Defi model aims to simulate the Olympous architechture of defi into its token AAAOHM or AHM.

The model offers users to bond with DAI and receive AHM. The Owner of the protocol can vary the crucial parameters which affect the behavior in the system.

What happens inside of simulation?
    
    1. Users are created with intial balnces of "DAI": 10000,"AHM": 0, "sAHM": 0, "ETH": 0
    2. DAI Bond is launched with BCV Adjustment Parameters and Bond Terms.
    3. The deployer deposits 90,000 DAI to treasury; 6,000 AHM gets minted to deployer and 84,000 DAI are in treasury as excesss reserves (RFV of AHM is set to 1 DAI by deployer)
    4. Staking contract is activated with staking parameters
    5. Revenue module is initiated to add profits to tresury

## Parameters

Bond Terms:

    - bond control variable (BCV): scaling variable for price
    - vesting term: vesting period for bond payout (in epochs)
    - min price: minimum price of bond, below which the bond can't be offered
    - fee: as a percent of bond payout, goes to treasury as portocol profits
    - max debt: maximum debt ratio allowed

BCV Adjustment Parameters:

    - rate: increment factor to BCV 
    - target: BCV when adjustment finished
    - buffer: minimum length (in epochs) between adjustments

Staking Parameter:

    - reward rate: percent of excess reserves to distribute as rebase rewards 
    - rebase period: frequency (in epochs) to rebase

## Module behaviors

### 1. Treasury
A Treasury has following baskets:
- Reserve assets from reserve bonds
- LP token assets from LP bonds

To manage treasury efficiently, Treasury has following split ratios:
- Reserve: 0.2 ; As a reserve assets inside treasury
- LP: 0.6 ; As a LP assets inside treasury generating revenue as LP rewards
- Lend: 0.2 ; As a lend assets inside treasury generating revenue from fiat loans to Vendors

### 2. Revenue
This classes manages revenue stream for the treasury
Two types of revenue streams:
1. LP rewards
2. Fiat Loan Revenue

> In our current model, we only accrue hypothetical profit, i.e. 6% APY on 60% of DAI holdings in our treasury   

## Results
Displays charts over epochs ran on
- Treasury
- User Balance (all users have identical behaviors)
- Total debt

