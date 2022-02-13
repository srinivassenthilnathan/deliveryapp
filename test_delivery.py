import unittest
from unittest.mock import patch
from calculate_cost import calculate_package_costs
from calculate_time import calculate_cost_time


class TestDelivery(unittest.TestCase):
    
    package_input1 = ["100 3",
                      "PKG1 5 5 OFR001",
                      "PKG2 15 5 OFR002",
                      "PKG3 10 100 OFR003"]
    
    package_cost_output1 = [{'package_id': 'PKG1', 'total_cost': 175, 'discount': 0},
                            {'package_id': 'PKG2', 'total_cost': 275, 'discount': 0},
                            {'package_id': 'PKG3', 'total_cost': 665, 'discount': 35}]
    
    package_input2 = ["100 5",
                      "PKG1 50 30 OFR001",
                      "PKG2 75 125 OFR0008",
                      "PKG3 175 100 OFR003",
                      "PKG4 110 60 OFR002",
                      "PKG5 155 95 NA",
                      "2 70 200"]
    
    package_cost_output2 = [{'pack_id': 'PKG2', 'discount': 0, 'total_cost': 1475, 'time': 1.79},
                            {'pack_id': 'PKG4', 'discount': 105, 'total_cost': 1395, 'time': 0.86},
                            {'pack_id': 'PKG3', 'discount': 0, 'total_cost': 2350, 'time': 1.43},
                            {'pack_id': 'PKG5', 'discount': 0, 'total_cost': 2125, 'time': 4.22},
                            {'pack_id': 'PKG1', 'discount': 0, 'total_cost': 750, 'time': 4.0}]
        
    @patch('builtins.input', side_effect=package_input1)
    def test_delivery_cost(self, mock_inputs):
        result = calculate_package_costs()
        self.assertEqual(result, self.package_cost_output1)
    
    @patch('builtins.input', side_effect=package_input2)
    def test_delivery_time(self, mock_inputs):
        result = calculate_cost_time()
        self.assertEqual(result, self.package_cost_output2)


if __name__ == '__main__':
    unittest.main()
