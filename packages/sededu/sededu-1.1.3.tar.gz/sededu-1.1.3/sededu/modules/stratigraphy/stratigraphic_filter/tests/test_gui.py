import pytest
import platform

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np
import matplotlib
# import stratigraphic_filter.stratigraphic_filter


T = 50
dt = 1
t = np.array(np.linspace(0, T, T+1/dt))


def test_pass():
    '''dummy test to give travis something to do'''
    assert True


# def test_generate_elevation():
#     from stratigraphic_filter.functions import generate_elevation

#     mu = 0
#     sigma = 1
#     elev = generate_elevation(mu, sigma)
#     assert True


# @pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
# def test_change_Qw_slider():

#     import stratigraphic_filter.stratigraphic_filter

#     gui = GUI()
#     gui.sm.slide_Qw.set_val(gui.config.Qwmax)
#     gui.fig.canvas.draw_idle()

#     return gui.fig



# @pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
# def test_change_sig_slider():

#     import stratigraphic_filter.stratigraphic_filter

#     gui = GUI()
#     gui.sm.slide_sig.set_val(gui.config.sigmax)
#     gui.fig.canvas.draw_idle()

#     return gui.fig



# @pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
# def test_change_Ta_slider():

#     import stratigraphic_filter.stratigraphic_filter

#     gui = GUI()
#     gui.sm.slide_Ta.set_val(gui.config.Tamax)
#     gui.fig.canvas.draw_idle()

#     return gui.fig



# @pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
# def test_change_yView_slider():

#     import stratigraphic_filter.stratigraphic_filter

#     gui = GUI()
#     gui.sm.slide_yView.set_val(gui.config.yViewmax)
#     gui.fig.canvas.draw_idle()

#     return gui.fig



# @pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
# def test_change_Bb_slider():

#     import stratigraphic_filter.stratigraphic_filter

#     gui = GUI()
#     gui.sm.slide_Bb.set_val(gui.config.Bbmax)
#     gui.fig.canvas.draw_idle()

#     return gui.fig


# @pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
# def test_change_rad_col():

#     import stratigraphic_filter.stratigraphic_filter

#     gui = GUI()
#     gui.sm.rad_col.set_active(2)
#     gui.fig.canvas.draw_idle()

#     return gui.fig
