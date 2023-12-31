import numpy as np
import sys as sys
import configparser as cp
from chemical_potential_free_energy import chemical_potential, free_energy, average_chemical_potential_and_concentration
from CahnHilliard_equation import Cahn_Hilliard_equation_integration
from create_initial_config import create_initial_config

#-----------------------------READ SIMULATION CONFIGURATION FROM FILE------------------------------------
#Import configuration parameters from simulation_configuration.txt file
config = cp.ConfigParser()
config.read(sys.argv[1])

#-----------------------------------INITIALIZE INPUT PARAMETERS-------------------------------------------
# Microstructure geometry

N = int(config.get('microstructure_settings', 'N'))            # number of subcells per cartesian direction
dx = float(config.get('microstructure_settings', 'dx'))        # dimension of subcell in x direction
dy = float(config.get('microstructure_settings', 'dy'))        # dimension of subcell in y direction

#Material  specific parameters

M = float(config.get('microstructure_settings', 'M'))                         # mobility
grad_coeff = float(config.get('microstructure_settings', 'grad_coeff'))       # gradient coefficient
A = float(config.get('microstructure_settings', 'A'))                         # multiplicative constant of free energy

# Concentration parameters

c0 = float(config.get('microstructure_settings', 'c0'))               # initial equilibrium concentration
c_noise = float(config.get('microstructure_settings', 'c_noise'))     # perturbation amplitude

# Time integration parameters

t0 = float(config.get('time_settings', 't0'))                     # starting time
dt = float(config.get('time_settings', 'dt'))                     # time step
n_iterations = int(config.get('time_settings', 'n_iterations'))   # number of time steps

# Seed option

seed_option = bool(config.get('simulation_seed', 'seed_option'))   

#if seed option is True, set seed specified by the user
if seed_option:
    seed = int(config.get('simulation_seed', 'seed'))
    np.random.seed(seed)

# Destinations for data saving

c_grid_datasave = config.get('data_paths', 'c_config_datasave')
aver_quantities_datasave = config.get('data_paths', 'aver_quantities_datasave')
#----------------------------------CREATE INITIAL STATE--------------------------------------------------------

# Build initial microstructure concentration grid

c = create_initial_config(N, c0, c_noise)

#compute initial free energy, average concentration and average chemical potential

average_chem_potential, average_c = average_chemical_potential_and_concentration(c, chemical_potential(c,A), N)
free_E = free_energy(c, A , grad_coeff, dx, dy)

#-----------------------------------PREPARE FILES TO STORE SIMULATED DATA---------------------------------
#open file to write the simulated concentration data and average quantities

with open(c_grid_datasave, "w") as data_config_file, open(aver_quantities_datasave, "w") as data_average_param_file:
    column_names_string = ["Time"]
    config_data_string = [str(t0)]
#write column names
    for l in range(0, N):
        for j in range(0, N):
            column_names_string.append(f"c_{l}_{j}")
    column_names_string.append('\n')
    data_config_file.write(' '.join(column_names_string))

#print initial concentration values
    for l in range(0, N):
        for j in range(0, N):
            config_data_string.append(str(c[l,j]))
    config_data_string.append('\n')
    data_config_file.write(' '.join(config_data_string))

#open file to write separately average concentration, average chem. potential and free energy
    column_names_string = "Time AverageConcentration AverageChem.Potential FreeEnergy\n"
    data_average_param_file.write(column_names_string)

#write initial values in file (with time indicator) 
    string_to_print = [str(t0),str(average_c),str(average_chem_potential),str(free_E),"\n"]
    data_average_param_file.write(' '.join(string_to_print))


#----------------------------------------SIMULATION--------------------------------------------------------
# Perform time evolution with time step dt for n_iterations 

    for i in range(1,n_iterations+1):
        #update time value
        t = t0 + i*dt

    #update concentration integrating Cahn-Hilliard equation
        c = Cahn_Hilliard_equation_integration(c, A, grad_coeff, dx, dy, M, dt)

    #print new configuration data to file (with time indicator)
        config_data_string = [str(t)]
        for l in range(0, N):
            for j in range(0, N):
                config_data_string.append(str(c[l,j]))
        config_data_string.append('\n')
        data_config_file.write(' '.join(config_data_string))

    #compute physical quantities of new configuration
        average_chem_potential, average_c = average_chemical_potential_and_concentration(c, chemical_potential(c, A), N)
        free_E = free_energy(c, A, grad_coeff, dx, dy)

    #print physical quantities to file (with time indicator) 
        string_to_print = [str(t),str(average_c),str(average_chem_potential),str(free_E),"\n"]
        data_average_param_file.write(' '.join(string_to_print))

    #print simulation status on the command line
        sys.stdout.write("\r Simulation running: {:.1f}%".format(i/n_iterations*100))
