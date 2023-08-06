import pytest

import eppy_funcs as ef
from evaluator import EvaluatorEP, EvaluatorSR
from parameters import RangeParameter, CategoryParameter, Parameter, FieldSelector, expand_plist
from problem import EPProblem, Problem
import sampling


@pytest.fixture
def building():
    return ef.get_building()
    #return ef.get_building('D:/EnergyPlusV9-0-1/ExampleFiles/SingleFamilyHouse_TwoSpeed_CutoutTemperature.idf')


@pytest.fixture
def parameters():
    parameters = [
        #Parameter(FieldSelector(object_name='HOUSE OCCUPANCY',
        #        field_name='Field 4'),
        #        value_descriptor=CategoryParameter([1.0]))
        Parameter(FieldSelector(object_name='NonRes Fixed Assembly Window',
                field_name='Solar Heat Gain Coefficient'),
                value_descriptor=RangeParameter(0.01,0.99))
        ]
    return parameters


@pytest.fixture
def problem(parameters):
    objectives = ['Electricity:Facility']
    problem = EPProblem(parameters, objectives)
    return problem


def test_eval(building, problem):
    print(type(building))
    evaluator = EvaluatorEP(problem, building)
    samples = sampling.dist_sampler(sampling.seeded_sampler, problem, 20)

    outputs = evaluator.df_apply(samples, keep_input=True)
    print()
    print(outputs)
    assert 0
