sim_conf = {
    "days": 60,
    "user_count": 50,
    "bond_count": 1,

    ## USER
    "user_config":{

        "balances":{
            'DAI': 10000,
            'AHM': 0,
            'sAHM': 0,
            'ETH': 0,
        }
        },
    ## TREASURY
    "treasury_config":{
        "staked_native_assets":{

        }
    },

    ## staking_AHM

    # "staking_AHM_config":{
    #     "sAHM":0,
    # }

    ## BOND config
    "bond_config":{
        'bond_term':{
            'bond_control_variable': 0, # Bonds must be initialized from 0
            'vesting_term': 5, #epoch (day) ; at least 36 hrs
            'min_price': 0.8,
            'max_payout': 10000, # 0.5% , can't be above 1%
            'fee': 2, # % goes to AAA Treasury
            'max_debt': 0.6 #(max debt ratio allowed), max % total supply created as debt
        },
        'principle': 'DAI',
        'is_Liquidity_Bond': False, # true if LP bond
        'adjustment':{
            'add': True,
            'rate': 0.02,
            'target': 0.2,
            'buffer': 2,
            'lastBlock': 0
        },

    }
    
}
