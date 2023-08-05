# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_tunisia.model.base import *
from openfisca_tunisia import entities

from numpy.ma.testutils import assert_not_equal

try:
    from urllib.request import Request  # python 3.0 and later
except ImportError:
    from urllib2 import Request  # python 2

try:
    from scipy.optimize import fsolve
except ImportError:
    fsolve = None


def calculate_net_from(salaire_imposable, individu, period, requested_variable_names):
    # We're not wanting to calculate salaire_imposable again, but instead manually set it as an input variable
    individu.get_holder('salaire_imposable').put_in_cache(salaire_imposable, period)

    # Work in isolation
    temp_simulation = individu.simulation.clone()
    temp_individu = temp_simulation.individu

    # Calculated variable holders might contain undesired cache
    # (their entity.simulation points to the original simulation above)
    for name in requested_variable_names:
        temp_individu.get_holder(name).delete_arrays()

    # Force recomputing of salaire_net_a_payer
    temp_individu.get_holder('salaire_net_a_payer').delete_arrays()
    net = temp_individu('salaire_net_a_payer', period)[0]

    return net


class salaire_imposable(Variable):
    value_type = float
    entity = Individu
    label = u"Salaire imposable"
    definition_period = MONTH
    set_input = set_input_divide_by_period


    def formula(individu, period):
        # Calcule le salaire imposable à partir du salaire net par inversion numérique.
        net = individu.get_holder('salaire_net_a_payer').get_array(period)
        if net is None:
            return individu.empty_array()

        simulation = individu.simulation
        simulation.period = period
        # List of variables already calculated. We will need it to remove their holders,
        # that might contain undesired cache
        requested_variable_names = list(simulation.requested_periods_by_variable_name.keys())
        if requested_variable_names:
            requested_variable_names.remove(u'salaire_imposable')
        # Clean 'requested_periods_by_variable_name', that is used by -core to check for computation cycles.
        # This variable, salaire_imposable, might have been called from variable X,
        # that will be calculated again in our iterations to compute the salaire_net_a_payer requested
        # as an input variable, hence producing a cycle error
        simulation.requested_periods_by_variable_name = dict()

        def solve_func(net):
            def innerfunc(essai):
                return calculate_net_from(essai, individu, period, requested_variable_names) - net
            return innerfunc

        imposable_calcule = \
            fsolve(
                solve_func(net),
                net * 1.25,  # on entend souvent parler cette méthode...
                xtol = 1 / 100  # précision
                )

        return imposable_calcule


class de_net_a_imposable(Reform):
    name = u'Inversion du calcul imposable -> net'

    def apply(self):
        self.update_variable(salaire_imposable)
