---
marp: true
---

This is test slide, made by ChatGPT

You have to install extension "Marp" for preview

---

# Simulating Ion Motion in Earth's Magnetic Field
### Using the Runge-Kutta Method

---

## Program Overview

- The program, Runge-Kutta.cpp, simulates the motion of ions in the Earth's magnetic field using the Runge-Kutta method.
- The program models the motion of two types of ions, oxygen and protons, and allows for the simulation of various initial conditions, such as the initial velocity and the strength of the electric field.
- The program also allows for the simulation of resonance acceleration, which occurs when the ion's velocity parallel to the magnetic field exceeds a certain threshold.
- The program outputs the results of the simulation in the form of a time plot of the ion's position and velocity.

---

## Defining Structs and Constants

- The program begins by defining a struct called "ion_type" which holds the name and mass of an ion.

- The program also defines two constants, massunit and oxygen, which are used to define the mass of the oxygen ion.

---

## Defining Simulation Parameters

- The program defines a number of parameters that are used in the simulation.
- These parameters include the ion being simulated, the strength of the electric field, the initial velocities of the ion, the maximum velocity parallel to the magnetic field for resonance acceleration, the duration of the resonance acceleration, and the period at which the resonance acceleration occurs.
- The program also defines a number of other parameters that are used in the calculation of the ion's motion, such as the L-shell of the Earth's magnetic field and the timestep used in the simulation.

---

## Defining Calculation Functions

- The program then defines several functions that are used in the calculation of the ion's motion.
- These functions include grad_field, which calculates the gradient of the magnetic field, and dlambda, which calculates the change in the ion's latitude.
- The program also defines two functions, dv_para and dv_perp, which calculate the change in the ion's velocity parallel and perpendicular to the magnetic field, respectively.

---

## Using the Runge-Kutta Method in the Main Function

- The program then uses the functions defined in the previous slides in the main function to simulate the ion's motion using the Runge-Kutta method.
- The program outputs the results of the simulation in the form of a time plot of the ion's position and velocity.

--- 

# Runge-Kutta method for simulating the motion of ions in the Earth's magnetic field

- The program models the motion of two types of ions, oxygen and protons
- Allows for the simulation of various initial conditions, such as the initial velocity and the strength of the electric field
- Allows for the simulation of resonance acceleration
- Outputs the results of the simulation in the form of a time plot of the ion's position and velocity

---

## Struct "ion_type"
- Holds the name and mass of an ion
- Two constants, massunit and oxygen, used to define the mass of the oxygen ion

---

## Simulation Parameters
- Ion being simulated
- Strength of the electric field
- Initial velocities of the ion
- Maximum velocity parallel to the magnetic field for resonance acceleration
- Duration of the resonance acceleration
- Period at which the resonance acceleration occurs

---

## Functions used in the calculation of the ion's motion
- grad_field: calculates the gradient of the magnetic field
- dlambda: calculates the change in the ion's latitude
- dv_para: calculates the change in the ion's velocity parallel to the magnetic field
- dv_perp: calculates the change in the ion's velocity perpendicular to the magnetic field

---

## Using the functions in the main function
- Runge-Kutta method is used to simulate the ion's motion
- Outputs the results of the simulation in the form of a time plot of the ion's position and velocity
