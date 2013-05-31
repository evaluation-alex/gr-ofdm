#!/usr/bin/env python

from gnuradio import gr
from ofdm_swig import moms_ff


################################################################################
################################################################################

class moms(gr.hier_block2):
  def __init__(self,delay_num,delay_denom):
    gr.hier_block2.__init__(self,"moms",
      gr.io_signature(1,1,gr.sizeof_gr_complex),
      gr.io_signature(1,1,gr.sizeof_gr_complex))

    cmplx_to_real  = gr.complex_to_real()
    cmplx_to_img   = gr.complex_to_imag()

    iirf_real = gr.iir_filter_ffd([1.5],[1, -0.5])
    self.moms_real = moms_ff()
    self.moms_real.set_init_ip_fraction(delay_num,delay_denom)

    iirf_imag = gr.iir_filter_ffd([1.5],[1, -0.5])
    self.moms_imag = moms_ff()
    self.moms_imag.set_init_ip_fraction(delay_num,delay_denom)

    float_to_cmplx = gr.float_to_complex()

    self.connect((self,0),            (cmplx_to_real,0))
    self.connect((self,0),            (cmplx_to_img,0))
    self.connect((cmplx_to_real,0),   (iirf_real,0))
    self.connect((cmplx_to_img,0),    (iirf_imag,0))
    self.connect((iirf_real,0),       (self.moms_real,0))
    self.connect((iirf_imag,0),       (self.moms_imag,0))
    self.connect((self.moms_real,0),  (float_to_cmplx,0))
    self.connect((self.moms_imag,0),  (float_to_cmplx,1))
    self.connect((float_to_cmplx,0),  (self,0))

  def get_ip_fraction_num(self):
    self.moms_real.get_ip_fraction_num()
  def get_ip_fraction_denom(self):
    self.moms_real.get_ip_fraction_denom()
  def get_offset_num(self):
    self.moms_real.get_offset_num()
  def set_ip_fraction(self,a,b):
    self.moms_real.set_ip_fraction(a,b)
    self.moms_imag.set_ip_fraction(a,b)
  def set_offset_num(self,a):
    self.moms_real.set_offset_num(a)
    self.moms_imag.set_offset_num(a)
