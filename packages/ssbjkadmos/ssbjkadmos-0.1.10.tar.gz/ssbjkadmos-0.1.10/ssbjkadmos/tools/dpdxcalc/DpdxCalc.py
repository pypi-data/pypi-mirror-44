#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SSBJ test case - http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19980234657.pdf
Original Python implementation for OpenMDAO integration developed by
Sylvain Dubreuil and Remi Lafage of ONERA, the French Aerospace Lab.
Original files taken from: https://github.com/OneraHub/SSBJ-OpenMDAO
The files were adjusted for optimal use in KADMOS by Imco van Gent of TU Delft.
"""
from __future__ import absolute_import, division, print_function

import sys

import numpy as np

from lxml import etree

from openlego.partials.partials import Partials
from openlego.utils.xml_utils import xml_safe_create_element

from ssbjkadmos.config import root_tag, x_tc, x_dpdx
from ssbjkadmos.tools.SsbjDiscipline import SsbjDiscipline
from ssbjkadmos.utils.math import polynomial_function, get_d_dict


class DpdxCalc(SsbjDiscipline):  # AbstractDiscipline

    @property
    def description(self):
        return u'Separate dpdx calculation if this calculation is required as separate constraint (e.g. in BLISS-2000).'

    @property
    def supplies_partials(self):
        return True

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_tc, self.get_default_value(x_tc))

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_dpdx, self.get_default_value(x_dpdx))

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_dpdx, [x_tc])
        return partials.get_string()

    def execute(self, in_file, out_file):
        doc = etree.parse(in_file)
        z0 = self.unscale_float_value(x_tc, doc)

        dpdx = dpdx_calc(np.array([z0, 0., 0., 0., 0., 0.]))

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_dpdx, self.scale_value(dpdx, x_dpdx))
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def linearize(self, in_file, partials_file):
        doc = etree.parse(in_file)
        z0 = self.unscale_float_value(x_tc, doc)

        # Execute ONERA partials function
        J_dpdx = dpdx_partials(dict(z=np.array([z0, 0., 0., 0., 0., 0.])), scalers=self.scalers)

        # Declare and write partials
        partials = Partials()
        partials.declare_partials(x_dpdx, [x_tc], [J_dpdx['z'][0, 0]])
        partials.write(partials_file)


def dpdx_calc(Z):
    # dpdx calculation as taken from the ONERA repository
    dpdx = polynomial_function([Z[0]], [1], [.25], "dpdx")
    return dpdx


def dpdx_partials(inputs, scalers):
    # dpdx partial calculation from ONERA repository
    # Removed self, J, scalers
    # Get d dictionary as static value
    Z = inputs['z']
    pf_d = get_d_dict()

    # dpdx ################################################################
    J_dpdx = dict()
    J_dpdx['z'] = np.zeros((1, 6))
    S_shifted, Ai, Aij = polynomial_function([Z[0]], [1], [.25], "dpdx", deriv=True)
    if Z[0] / pf_d['dpdx'][0] >= 0.75 and Z[0] / pf_d['dpdx'][0] <= 1.25:
        dStcdtc = 1.0 / pf_d['dpdx'][0]
    else:
        dStcdtc = 0.0
    dStcdtc2 = 2.0 * S_shifted[0] * dStcdtc
    ddpdxdtc = Ai[0] * dStcdtc + 0.5 * Aij[0, 0] * dStcdtc2
    J_dpdx['z'][0, 0] = ddpdxdtc/scalers['dpdx']*scalers['tc']

    return J_dpdx


if __name__ == "__main__":

    DpdxCalc().run_tool(sys.argv)
