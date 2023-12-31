import numpy as np
from create_initial_config import create_initial_config
from hypothesis import given
import hypothesis.strategies as st
import pytest as pt

@given(N=st.integers(min_value=2, max_value=100), c_0=st.floats(min_value=0, max_value=1))
def test_initState_is_c_0_if_noise_is_0(N, c_0):
    """this function tests that if c_noise is null, the initial configuration 
       is an array of Nx-by-Ny c_0

       GIVEN: c_noise=0,N,c_0 randomly picked numbers 
       WHEN: they are provided as parameters to create_initial_config()
       THEN: function returs initState with all elements equal to c_0"""

    c_noise=0.
    constant_array=np.full((N,N), c_0)
    np.random.seed(1)
    initial_config=create_initial_config(N,c_0, c_noise)
    assert np.array_equal(constant_array, initial_config)

@given(c_0=st.floats(min_value=0, max_value=1), c_noise=st.floats(min_value=0, max_value=1), N = st.floats())
def test_initState_fails_for_incorrect_NxNy_parameters(c_0, c_noise, N):
    """this function tests that if incorrect Nx, Ny parameters are given to create_initial_config(), 
       the function raises an error

       GIVEN: N randomly picked real numbers 
       WHEN: they are provided as parameters to create_initial_config()
       THEN: function raises TypeError"""
    np.random.seed(1)
    with pt.raises(TypeError):
       create_initial_config(N,c_0,c_noise)

@given(c_0=st.floats(min_value=1.1), c_noise=st.floats(max_value=1.1), N=st.integers(min_value=2,max_value=100))
def test_initState_fails_for_incorrect_c0cnoise_parameters(c_0, c_noise, N):
    """this function tests that if incorrect c_0, c_noise parameters are given to create_initial_config(), 
       the function raises an error

       GIVEN: c_0, c_noise randomly picked real numbers 
       WHEN: they are provided as parameters to create_initial_config()
       THEN: function raises ValueError"""
    np.random.seed(1)
    with pt.raises(ValueError):
       create_initial_config(N,c_0,c_noise)

@given(c_0=st.floats(min_value=0, max_value=1), c_noise=st.floats(min_value=0, max_value=1))
def test_function_fails_for_null_cell_parameters(c_0, c_noise):
    """this function tests that create_initial_config() raises an error for Nx=0, Ny=0

       GIVEN: null supercell dimensions parameters 
       WHEN: they are provided as parameters to create_initial_config()
       THEN: function raises ValueError"""
    N=0
    np.random.seed(1)
    with pt.raises(ValueError):
       create_initial_config(N,c_0,c_noise)

def test_invalid_initState_raise_error():
   """ This function tests that if c_0 and c_noise produce negative subcell concentrations,
       create_initial_config() raises an error
       
       GIVEN: c_0 = 0, only concentration fluctuation present, standard Nx, Ny values
       WHEN: they are provided to create_initial_config()
       THEN: function raises ValueError
       """

   N= 1000
   c_0= 0.
   c_noise=1.
   np.random.seed(1)
   with pt.raises(ValueError):
      create_initial_config(N, c_0, c_noise)

def test_initState_is_repeatable():
   """ This function tests that the initial config. produced by create_initial_config() is repeatable 
       
       GIVEN: fixed N,c_0,c_noise values
       WHEN: they are provided two times to create_initial_config() and same seed is selected for each function call
       THEN: function produces the same output
       """
   N=100
   c_0=0.5
   c_noise=0.02
   np.random.seed(1)
   initState_1 = create_initial_config(N, c_0, c_noise)
   np.random.seed(1)
   initState_2 = create_initial_config(N, c_0, c_noise)
   assert np.array_equal(initState_1, initState_2)

def test_initStat_is_physical_configuration():
    """This function tests that if the concentration configuration obtained as output of create_initial_config() 
    with physical input parameters has values in the interval [0,1]
    
       GIVEN: fixed Nx,Ny,c_0,c_noise values
       WHEN: they are provided two times to create_initial_config()
       THEN: function produces an N-by-N 2D array with all values in [0,1] """

    N=100
    c_0=0.5
    c_noise=0.02
    np.random.seed(1)
    initState = create_initial_config(N, c_0, c_noise)
    initState_validity = np.logical_and(initState>=0, initState<=1)
    assert initState.all()