Simulation
==========

Running the Simulation Locally
------------------------------

To use the simulator, first install the Poetry prerequisites:

.. code-block:: console

   (.venv) $ poetry install


----------------

To begin a simulation,
you can use the ``sim_hander.run()`` function:

.. autofunction:: aaa.sim_handler.SimHandler.run
 

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
will raise an exception.

.. py:exception:: lumache.InvalidKindError
   Raised if the kind is invalid.

>>> import lumache
>>> lumache.get_random_ingredients()
['shells', 'gorgonzola', 'parsley']


