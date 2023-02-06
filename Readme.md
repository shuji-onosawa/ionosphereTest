# Calculate between mirror force and some acceleration for v_perp

## Environment
You need 

- g++ (for c++)

- python3 (for python)

- python library
    - pandas
    - matplotlib

- VSCode (for build and run)

- VSCode extension
    - C/C++
    - C/C++ Extension Pack

- gdb (for debug)

We develop this code using WSL2, so if you use other OS or environment, you should rewrite some code.

I use https://qiita.com/firedfly/items/00c34018581c6cec9b84 for clean Python code.

---

## Run

on VSCode

Build and run → Ctrl + Shift + B

if you want debug, you push f5 key.

You can read markdown text with Ctrl+k→v

---

## Parameter

You open src/Runge-Kutta.cpp and rewrite Lines 18-29.

Be careful : 

If you rewrite some parameter, output graph's name is changed, but some other parameter, it is not.

---

## Folder
- data 
    - output data
- doc 
    - Simulation document, like basic equations
- execute
    - folder for execture file
- graphs
    - graphs...
- src
    - soruce code
---

## Equation
you read doc folder.


## Library
We use 
https://github.com/nlohmann/json/blob/develop/include/nlohmann/json.hpp
for json include
(you **dont't** have to install this.
 But, We use this in src/json.hpp)