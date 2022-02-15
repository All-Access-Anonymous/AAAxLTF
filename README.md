# AAA tokenomics

[![GitHub Super-Linter](https://github.com/longtailfinancial/aaa-tokenomics/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

Modelling tokenomics similar to https://fantohm.com/ for our use case.

## Basic Concept
This concept can be changed
```
#Simulate per seat tiers
for tier in seat_tiers:

    for day in purchase_period:
    
        #Simulate attendees buying tickets
        for attendee in attendees:
            # Decide if attendee is going to buy a seat
            if buy_seat:
                # Buy seat
        
        #Increase ticket price
```

## AAA Model Diagrams:

https://miro.com/app/board/uXjVOXwHq1M=/

## Reading Resources on OHM model:

https://www.jordanmmck.com/crypto/olympus-dao?s=09

https://0xkowloon.substack.com/p/dissecting-the-olympus-protocol

https://forum.olympusdao.finance/d/77-oip-18-reward-rate-framework-and-reduction


# Development

## Requirements:
Python >= 3.10  
[Virtualfish](https://virtualfish.readthedocs.io/en/latest/install.html)  

## Installation: 
```
# Start new virtual fish environment (you can replace 'AAA' into something you prefer)
$ vf new AAA

# Activate the new environment
$ vf activate AAA

# Run the project
$ python -m aaa.[the_main_module]
```

## Progress:
- [ ] Implement visual presentation of the simulation
- [ ] Add dynamic simulation state configuration (seats tiers, ticket price increase and purchase probability)
- [ ] Bring back Github Actions with better code linter
- [x] Build the skeleton of the simulation (concert attendee and market)

## Warning:

There is currently an issue with pip's format when doing "pip freeze".
Refer to this thread:

https://stackoverflow.com/questions/62885911/pip-freeze-creates-some-weird-path-instead-of-the-package-version

Solution is to simply use:
```
pip list --format=freeze > requirements.txt
```

instead of pip freeze.
