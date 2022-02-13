import sys
from calculate_cost import calculate_package_costs
from calculate_time import calculate_cost_time

if __name__ == "__main__":
    
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'time':
            calculate_cost_time()
        elif sys.argv[1] == 'cost':
            calculate_package_costs()
        else:
            print("Please choose between cost and time")
    else:
        print("Please specify a parameter(time/cost) after the python file name")
