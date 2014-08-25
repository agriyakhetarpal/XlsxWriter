###############################################################################
#
# Tests for XlsxWriter.
#
# Copyright (c), 2013-2014, John McNamara, jmcnamara@cpan.org
#

import unittest
import os
from ...workbook import Workbook
from ..helperfunctions import _compare_xlsx_files


class TestCompareXLSXFiles(unittest.TestCase):
    """
    Test file created by XlsxWriter against a file created by Excel.

    """

    def setUp(self):
        self.maxDiff = None

        filename = 'chart_chartarea04.xlsx'

        test_dir = 'xlsxwriter/test/comparison/'
        self.got_filename = test_dir + '_test_' + filename
        self.exp_filename = test_dir + 'xlsx_files/' + filename

        self.ignore_files = []
        self.ignore_elements = {'xl/charts/chart1.xml': ['<c:formatCode']}

    def test_create_file(self):
        """Test XlsxWriter gridlines."""
        filename = self.got_filename

        ####################################################

        workbook = Workbook(filename)

        worksheet = workbook.add_worksheet()
        chart = workbook.add_chart({'type': 'stock'})
        date_format = workbook.add_format({'num_format': 14})

        chart.axis_ids = [82954112, 82956288]

        data = [
            [39083, 39084, 39085, 39086, 39087],
            [27.2, 25.03, 19.05, 20.34, 18.5],
            [23.49, 19.55, 15.12, 17.84, 16.34],
            [25.45, 23.05, 17.32, 20.45, 17.34],
        ]

        for row in range(5):
            worksheet.write(row, 0, data[0][row], date_format)
            worksheet.write(row, 1, data[1][row])
            worksheet.write(row, 2, data[2][row])
            worksheet.write(row, 3, data[3][row])

        worksheet.set_column('A:D', 11)

        chart.add_series({
            'categories': '=Sheet1!$A$1:$A$5',
            'values': '=Sheet1!$B$1:$B$5',
        })

        chart.add_series({
            'categories': '=Sheet1!$A$1:$A$5',
            'values': '=Sheet1!$C$1:$C$5',
        })

        chart.add_series({
            'categories': '=Sheet1!$A$1:$A$5',
            'values': '=Sheet1!$D$1:$D$5',
        })

        chart.set_chartarea({
            'border': {'color': '#FF0000'},
            'fill': {'color': '#00B050'}
        })

        chart.set_plotarea({
            'border': {'dash_type': 'dash_dot'},
            'fill': {'color': '#FFC000'}
        })

        worksheet.insert_chart('E9', chart)

        workbook.close()

        ####################################################

        got, exp = _compare_xlsx_files(self.got_filename,
                                       self.exp_filename,
                                       self.ignore_files,
                                       self.ignore_elements)

        self.assertEqual(got, exp)

    def tearDown(self):
        # Cleanup.
        if os.path.exists(self.got_filename):
            os.remove(self.got_filename)
