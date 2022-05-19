# AAA tokenomics

Protocol simulation https://my.machinations.io/d/AAA-PID-Controller/8a231d5caf7411ec8c2902f943517e50

Tokenomic Report https://hackmd.io/J2NeJ-usReSFplZ6dbrJqQ

## BaseTen models and apps

Bond simulation https://app.baseten.co/applications/VqK33qo/operator_views/Q04Lz0d

Ticket sales simulaiton https://app.baseten.co/applications/b0dVjqn/operator_views/eP39pBJ

Liquidity Bootstrap Pool simulator https://www.ltf.dev/

Modelling tokenomics similar to https://fantohm.com/ for our use case.

## AAA Model Diagrams

https://miro.com/app/board/uXjVOXwHq1M=/

## Reading Resources on OHM model

https://www.jordanmmck.com/crypto/olympus-dao?s=09

https://0xkowloon.substack.com/p/dissecting-the-olympus-protocol

https://forum.olympusdao.finance/d/77-oip-18-reward-rate-framework-and-reduction

# Jupyter Notebook Usage
1. Create virtual fish environment.  
`$ vf new aaa`  
1.1.(Optional) Connect that virtual environment to working directory.  This eliminates
the need to type virutal fish environment activate command. `$vf connect`
2. Download & install required packages.  
`$ python3 -m pip install -r requirements.txt`  
3. Add virtual fish environment to Jupyter kernel.
[More detailed guide](https://janakiev.com/blog/jupyter-virtual-envs/)  
`python3 -m pip install --user ipykernel`  
`python3 -m ipykernel install --user --name=aaa`
4. Fire up Jupyter Notebook and you are good to go. :thumbsup:  
`$ jupyter notebook`

# Deployment
To be able to install aaa-tokenomics as Python pakcage, you need to have ssh-key setup with Github and proper access rights to this repo.  

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
## Updating package
```
# Install updated package
$ python3 -m pip install --update aaa
```

## Development
Update package requirements at pyproject.toml if you have installed or updated a
python package.

Edit the package version if you have changed anything.  


## Warning

There is currently an issue with pip's format when doing "pip freeze".
Refer to this thread:

https://stackoverflow.com/questions/62885911/pip-freeze-creates-some-weird-path-instead-of-the-package-version

Solution is to simply use:
```
pip list --format=freeze > requirements.txt
```

instead of pip freeze.
