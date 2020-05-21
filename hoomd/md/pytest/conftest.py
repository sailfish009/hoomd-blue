import hoomd
import pytest
import numpy as np
from copy import deepcopy
import itertools

_pairs = [
    ["Gauss",
     hoomd.md.pair.Gauss(hoomd.md.nlist.Cell()),
     {'epsilon': 0.05, "sigma": 0.02}],
    ["LJ",
     hoomd.md.pair.LJ(hoomd.md.nlist.Cell()),
     {"epsilon": 0.0005, "sigma": 1}],
    ["Yukawa",
     hoomd.md.pair.Yukawa(hoomd.md.nlist.Cell()),
     {"epsilon": 0.0005, "kappa": 1}],
    ["Ewald",
     hoomd.md.pair.Ewald(hoomd.md.nlist.Cell()),
     {"alpha": 0.05, "kappa": 1}],
    ["Morse",
     hoomd.md.pair.Morse(hoomd.md.nlist.Cell()),
     {"D0": 0.05, "alpha": 1, "r0": 0}],
    ["DPDConservative",
     hoomd.md.pair.DPDConservative(hoomd.md.nlist.Cell()),
     {"A": 0.05}],
    ["ForceShiftedLJ",
     hoomd.md.pair.ForceShiftedLJ(hoomd.md.nlist.Cell()),
     {"epsilon": 0.0005, "sigma": 1}],
]


@pytest.fixture(scope='function', params=_pairs, ids=(lambda x: x[0]))
def pair_and_params(request):
    return deepcopy(request.param[1:])


def _lj_valid_params():
    particle_types_list = [['A'], ['A', 'B'],
                           ['A', 'B', 'C'],
                           ['A', 'B', 'C', 'D']]
    combos = []
    for particle_types in particle_types_list:
        type_combo = list(itertools.combinations_with_replacement(particle_types,
                                                                  2))
        combos.append(type_combo)
        N = len(type_combo)
    sample_range = np.linspace(0.5, 1.5, 100)
    samples = np.array_split(np.random.choice(sample_range,
                                              size=N * len(combos) * 3,
                                              replace=True), 3)
    pair_potential_dicts = []
    r_cut_dicts = []
    r_on_dicts = []
    count = 0
    for combo_list in combos:
        combo_pair_potentials = {}
        combo_rcuts = {}
        combo_rons = {}
        for combo in combo_list:
            combo_pair_potentials[tuple(combo)] = {'sigma': samples[0][count],
                                                   'epsilon': samples[1][count]}
            combo_rcuts[tuple(combo)] = 2.5 * samples[0][count]
            combo_rons[tuple(combo)] = 2.5 * samples[0][count] * samples[2][count]
            count += 1
        pair_potential_dicts.append(combo_pair_potentials)
        r_cut_dicts.append(combo_rcuts)
        r_on_dicts.append(combo_rons)

    pair_potential = [hoomd.md.pair.LJ] * len(combos)
    modes = np.random.choice(['none', 'shifted', 'xplor'], size=len(combos))

    return zip(pair_potential,
               pair_potential_dicts,
               r_cut_dicts,
               r_on_dicts,
               modes)


@pytest.fixture(scope="function", params=_lj_valid_params())
def valid_params(request):
    return deepcopy(request.param)

_lj_invalid_params = [(hoomd.md.pair.LJ,
                       {('A', 'A'): {'sigma': [1, 2], 'epsilon': 1.0}},
                       {('A', 'A'): 2.5},
                       {('A', 'A'): 2.1},
                       'none'),
                      (hoomd.md.pair.LJ,
                       {('A', 'A'): {'sigma': 1.0, 'epsilon': [1, 2]}},
                       {('A', 'A'): 2.5},
                       {('A', 'A'): 2.1},
                       'none'),
                      (hoomd.md.pair.LJ,
                       {('A', 'A'): {'sigma': 'str', 'epsilon': 1.0}},
                       {('A', 'A'): 2.5},
                       {('A', 'A'): 2.1},
                       'none'),
                      (hoomd.md.pair.LJ,
                       {('A', 'A'): {'sigma': 1.0, 'epsilon': 'str'}},
                       {('A', 'A'): 2.5},
                       {('A', 'A'): 2.1},
                       'none'),
                      (hoomd.md.pair.LJ,
                       {('A', 'A'): {'sigma': 1.0, 'epsilon': 1.0}},
                       {('A', 'A'): [1, 2]},
                       {('A', 'A'): 2.1},
                       'none'),
                      (hoomd.md.pair.LJ,
                       {('A', 'A'): {'sigma': 1.0, 'epsilon': 1.0}},
                       {('A', 'A'): 'str'},
                       {('A', 'A'): 2.1},
                       'none'),
                      (hoomd.md.pair.LJ,
                       {('A', 'A'): {'sigma': 1.0, 'epsilon': 1.0}},
                       {('A', 'A'): 2.5},
                       {('A', 'A'): [1, 2]},
                       'none'),
                      (hoomd.md.pair.LJ,
                       {('A', 'A'): {'sigma': 1.0, 'epsilon': 1.0}},
                       {('A', 'A'): 2.5},
                       {('A', 'A'): 'str'},
                       'none'),
                      (hoomd.md.pair.LJ,
                       {('A', 'A'): {'sigma': 1.0, 'epsilon': 1.0}},
                       {('A', 'A'): 2.5},
                       {('A', 'A'): 2.1},
                       5),
                      (hoomd.md.pair.LJ,
                       {3: {'sigma': 1.0, 'epsilon': 1.0}},
                       {3: 2.5},
                       {3: 2.1},
                       'none')]


@pytest.fixture(scope="function", params=_lj_invalid_params)
def invalid_params(request):
    return deepcopy(request.param)
