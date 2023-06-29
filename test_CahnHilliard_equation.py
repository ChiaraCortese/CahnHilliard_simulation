import numpy as np
from create_initial_config import create_initial_config
from chemical_potential_free_energy import chemical_potential
from concentration_laplacian import concentration_laplacian
from CahnHilliard_equation import Cahn_Hilliard_equation_integration
from hypothesis import given
import hypothesis.strategies as st
import pytest as pt

@given(dx=st.floats(min_value=0.1), dy=st.floats(min_value=0.1), k=st.floats(min_value=0.), A=st.floats(min_value=0.), M=st.floats(max_value = -0.001), dt=st.floats(max_value=-0.001))
def test_CahnHilliard_integration_fails_with_incorrect_M_dt_parametes(dx,dy,k,A, M, dt):
    """this function tests that if invalid M, dt parameters are given to Cahn_Hilliard_equation_integration(), 
       the functions raise an error

       GIVEN: A, k,dx, dy valid float numbers, a given concentration matrix c, negative M, dt
       WHEN: they are provided as parameters to Cahn_Hilliard_equation_integration()
       THEN: function raises ValueError"""
    N = 10
    c_0=0.5
    c_noise=0.02
    c=create_initial_config(N,c_0, c_noise)
    with pt.raises(ValueError):
       Cahn_Hilliard_equation_integration(c, A, k, dx, dy, M, dt)

def test_CahnHilliard_integration_returns_expected_values():
     """this function tests that if the initial concentration is the equilibrium one,
       Cahn_Hilliard_equation_integration() returns as the updated concentration value the initial one,
       for each subcell, in an array of same shape of the input concentration one 
    
    GIVEN: a 2-by-2 concentration grid with all values equal to 0.5, and A=1,M=1, k=1, dx=1, dy=1, dt=1
    WHEN: they are provided as input parameters to Cahn_Hilliard_equation_integration(),
    THEN: function returns a 2-by-2, 2D array with all elements equal to initial values"""

     N = 2
     A = 1
     dx = 1
     dy = 1
     k = 1
     M = 1
     dt = 1
     c = np.array([[0.5, 0.5],
                  [0.5, 0.5]])
     updated_c_computed = Cahn_Hilliard_equation_integration(c, A, k, dx, dy, M, dt)
     updated_c_expected = np.array([[0.5, 0.5],
                              [0.5, 0.5]])
     assert np.shape(updated_c_computed) == np.shape(c)
     for i in [0,N-1]:
         for j in [0,N-1]:
             assert updated_c_computed[i,j] == updated_c_expected[i,j]

def test_CahnHilliard_integration_fails_for_invalid_output_configuration():
    """This function tests that if the concentration configuration obtained by integrating the 
    Cahn-Hilliard equation is not valid, then the function raises an error.
    
    GIVEN: 2-by-2 concentration grid with a big concentration difference ([[0, 1], [1, 0]]), 
           A = k = dx = dy = M = dt = 1
    WHEN: they are provided as parameters to Cahn_Hilliard_equation_integration()
    THEN: function fails due to resulting concentration grid with values higher than 1"""

    N = 2
    A = 1
    dx = 1
    dy = 1
    k = 1
    M = 1
    dt = 1
    c = np.array([[0, 1], 
                 [1, 0]])
    with pt.raises(ValueError):
       Cahn_Hilliard_equation_integration(c, A, k, dx, dy, M, dt)