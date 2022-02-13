import unittest
from unittest.mock import patch
import utils


class TestUtils(unittest.TestCase):
    convert_input = ["PKG1 50 30 OFR001",
                     "PKG2 75 125 OFR0008",
                     "PKG3 175 100 OFR003",
                     "PKG4 110 60 OFR002",
                     "PKG5 155 95 NA"]
    
    convert_package_output = [{'package_id': 'PKG1', 'weight': 50, 'distance': 30, 'coupon_code': 'OFR001'},
                              {'package_id': 'PKG2', 'weight': 75, 'distance': 125, 'coupon_code': 'OFR0008'},
                              {'package_id': 'PKG3', 'weight': 175, 'distance': 100, 'coupon_code': 'OFR003'},
                              {'package_id': 'PKG4', 'weight': 110, 'distance': 60, 'coupon_code': 'OFR002'},
                              {'package_id': 'PKG5', 'weight': 155, 'distance': 95, 'coupon_code': 'NA'}]
    
    sort_output = [{'package_id': 'PKG1', 'weight': 50, 'distance': 30, 'coupon_code': 'OFR001'},
                   {'package_id': 'PKG2', 'weight': 75, 'distance': 125, 'coupon_code': 'OFR0008'},
                   {'package_id': 'PKG4', 'weight': 110, 'distance': 60, 'coupon_code': 'OFR002'},
                   {'package_id': 'PKG5', 'weight': 155, 'distance': 95, 'coupon_code': 'NA'},
                   {'package_id': 'PKG3', 'weight': 175, 'distance': 100, 'coupon_code': 'OFR003'}]
    
    estimate_combo_output = [{'package_id': 'PKG2', 'weight': 75, 'distance': 125, 'coupon_code': 'OFR0008'},
                             {'package_id': 'PKG4', 'weight': 110, 'distance': 60, 'coupon_code': 'OFR002'}]
    
    def test_validate_input(self):
        result = utils.validate_input(['1 2 3'], 3)
        self.assertIsNone(result)
        self.assertRaises(ValueError, utils.validate_input, ['1 2 3'], 4)
    
    def test_evaluate_condition(self):
        self.assertTrue(utils.evaluate_condition(60, '50-100'))
        self.assertFalse(utils.evaluate_condition(60, '>200'))
        self.assertTrue(utils.evaluate_condition(60, '<200'))
    
    def test_delivery_cost_discount(self):
        total_cost = utils.get_package_delivery_cost({"package_id": "PKG4", "weight": "110",
                                                      "distance": "60", "coupon_code": "OFR002"}, 100)
        self.assertEqual(total_cost, 1500)
        discount = utils.calculate_discount({"package_id": "PKG4", "weight": "110",
                                             "distance": "60", "coupon_code": "OFR002"}, total_cost)
        self.assertEqual(discount, 105)
    
    def test_sort_package(self):
        self.assertEqual(utils.sort_package(self.convert_package_output, 'weight'), self.sort_output)
    
    def test_convert_package_details(self):
        self.assertTrue(utils.convert_package_details(self.convert_input) == self.convert_package_output)
    
    def test_estimated_combo(self):
        
        self.assertTrue(utils.estimated_combo(self.sort_output, 200), self.estimate_combo_output)
    
    def test_get_package_delivery_time(self):
        self.assertEqual("{:.2f}".format(utils.get_package_delivery_time(self.sort_output, 70)), "1.79")


if __name__ == '__main__':
    unittest.main()
