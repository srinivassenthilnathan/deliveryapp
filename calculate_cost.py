from utils import convert_package_details, calculate_discount, get_package_delivery_cost, get_package_input


def calculate_cost(**kwargs):
    """
    To calculate cost of delivery for list of packages
    
    :param kwargs:
    base_delivery_cost - base delivery cost
    no_of_packages - number of packages
    package_details - details of package
    print_cost - should the function print cost of package
    
    :return delivery_costs: return list of packages with their delivery cost
    :rtype delivery_costs: list of dict
    """
    delivery_costs = []
    
    print("Package id, discount, total cost")
    
    for package_detail in kwargs['package_details']:
        delivery_cost = get_package_delivery_cost(package_detail, int(kwargs['base_delivery_cost']))
        discount = calculate_discount(package_detail, delivery_cost)
        delivery_costs.append({'package_id': package_detail['package_id'],
                               'total_cost': delivery_cost - discount, 'discount': discount})
        if kwargs['print_cost']:
            print(package_detail['package_id'], discount, delivery_cost - discount, sep=' ')
    return delivery_costs


def calculate_package_costs():
    """
    To get package details and call calculate delivery cost function
    
    :param:
    
    :return:
    """
    base_delivery_cost, no_of_packages, package_details = get_package_input()
    return calculate_cost(base_delivery_cost=base_delivery_cost,
                          no_of_packages=no_of_packages,
                          package_details=convert_package_details(package_details),
                          print_cost=True)
