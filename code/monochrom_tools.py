import jpegio
import math
import numpy
from file_path import get_path, get_restore_path

"""This module contains some function to manipulate the coefficients of the Y, 
Cb and Cr blocks in a 16*16 macroblock.
This modul takes heavy use of the jpegio module and works only for sampling 
sizes of 4:1:1 (22 11 11 as samplings-sizes in the SOF segment)"""

def make_left_mono(input):
    entropie = jpegio.read(get_path(input).as_posix())
    height, width = entropie.coef_arrays[1].shape
    half = math.ceil(width / 2) # In order to just manipulate the left half of blocks

    for m in range(height):
        for n in range(half):
            # Setting them 0 removes the Cb and Cr part of the block resulting in just luminance
            entropie.coef_arrays[1][m, n] = 0
            entropie.coef_arrays[2][m, n] = 0

    jpegio.write(entropie, get_restore_path(input, "left_mono").as_posix())

def swap_cb_cr(input):

    entropie = jpegio.read(get_path(input).as_posix())

    temp = entropie.coef_arrays[1][:]
    entropie.coef_arrays[1][:] = entropie.coef_arrays[2][:]  # Cb invertieren
    entropie.coef_arrays[2][:] = temp  # Cr invertieren


    jpegio.write(entropie, get_restore_path(input, "swapped_cb_cr").as_posix())

def make_negative(input):

    entropie = jpegio.read(get_path(input).as_posix())

    entropie.coef_arrays[1][:] = -entropie.coef_arrays[1][:]
    entropie.coef_arrays[2][:] = -entropie.coef_arrays[2][:]


    jpegio.write(entropie, get_restore_path(input, "negative").as_posix())

def make_mono(input):
    entropie = jpegio.read(get_path(input).as_posix())
    entropie.coef_arrays[1][:] = 0  
    entropie.coef_arrays[2][:] = 0  

    jpegio.write(entropie, get_restore_path(input, "mono").as_posix())

def make_all_types(input):
    make_left_mono(input) 
    swap_cb_cr(input)
    make_negative(input)
    make_mono(input)