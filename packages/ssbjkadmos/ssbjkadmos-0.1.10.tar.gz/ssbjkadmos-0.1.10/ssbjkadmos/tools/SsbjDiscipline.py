import inspect
import os
import sys

from kadmos.external.XML_merger.XMLmerger import merge_xmls
from openlego.core.abstract_discipline import AbstractDiscipline

from ssbjkadmos.tools import ssbj_scalers, ssbj_nonscalers, scale_values
from ssbjkadmos.utils.execution import get_args
from ssbjkadmos.utils.general import get_dict_name


class SsbjDiscipline(AbstractDiscipline):

    @property
    def name(self):
        # type: () -> str
        """:obj:`str`: Name of this discipline."""
        return self.__class__.__name__

    @property
    def creator(self):
        return u'S. Dubreuil and R. Lafage'

    @property
    def owner(self):
        return u'J. Sobieszczanski-Sobieski'

    @property
    def operator(self):
        return u'I. van Gent'

    @property
    def description(self):
        return u'Discipline of the SSBJ test case.'

    @property
    def version(self):
        return u'1.0'

    @property
    def path(self):
        # type: () -> str
        """:obj:`str`: Path at which this discipline resides."""
        return os.path.dirname(inspect.getfile(self.__class__))

    @property
    def scale_values(self):
        return scale_values

    @property
    def scalers(self):
        if self.scale_values:
            return ssbj_scalers
        else:
            return ssbj_nonscalers

    def run_tool(self, sys_argv):
        class_name = self.__class__.__name__
        class_name_lc = class_name.lower()

        args = get_args(sys_argv)

        out_file = args.out_file.format(class_name_lc)

        if args.test:
            in_file = '__test__{}_input.xml'.format(class_name_lc)
            with open(in_file, 'wb') as f:
                f.write(self.generate_input_xml())
            self.execute(in_file, out_file)
            sys.stdout.write('Executed test run of {}.py with input file "{}" and output file '
                             '"{}".\n'.format(class_name, in_file, out_file))
        else:
            in_file = args.in_file
            if not os.path.isfile(in_file):
                raise AssertionError('could not find the input file "{}" in the folder.'
                                     .format(in_file))
            self.execute(in_file, out_file)
            sys.stdout.write('Executed run of {}.py with input file "{}" and output file "{}".\n'
                             .format(class_name, in_file, out_file))
        if args.merge_files:
            merge_xmls([in_file, out_file], out_file)

    def generate_input_xml(self):
        raise NotImplementedError

    def generate_output_xml(self):
        raise NotImplementedError

    def get_scaler(self, xpath):
        return self.scalers[get_dict_name(xpath)]

    def scale_value(self, val, xpath):
        return val/self.scalers[get_dict_name(xpath)]

    def unscale_float_value(self, xpath, doc):
        return float(doc.xpath(xpath)[0].text) * self.scalers[get_dict_name(xpath)]

    def get_default_value(self, xpath):
        if self.scale_values:
            return ssbj_nonscalers[get_dict_name(xpath)]
        else:
            return ssbj_scalers[get_dict_name(xpath)]
