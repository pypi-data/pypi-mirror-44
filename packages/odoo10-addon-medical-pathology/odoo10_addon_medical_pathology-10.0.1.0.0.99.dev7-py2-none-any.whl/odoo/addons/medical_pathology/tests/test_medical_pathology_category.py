# -*- coding: utf-8 -*-
# Copyright 2008 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestMedicalPathologyCategory(TransactionCase):

    def setUp(self):
        super(TestMedicalPathologyCategory, self).setUp()
        self.pathology_category_1 = self.env.ref(
            'medical_pathology.medical_pathology_category_1'
        )

    def test_check_recursive_parent(self):
        """ Test category recursive parent raises ValidationError """
        with self.assertRaises(ValidationError):
            self.pathology_category_1.parent_id = self.env.ref(
                'medical_pathology.medical_pathology_category_2'
            ).id
