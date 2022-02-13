import utils


def get_vehicle_input():
    """
    To get vehicle details from user
    
    :param:
    
    :return vehicle_details:
    :rtype vehicle_details: basestring
    """
    try:
        print("Please enter number of vehicles, max speed and max weight per vehicle: ")
        vehicle_details = input()
        
        utils.validate_input([vehicle_details], 3)
        return vehicle_details
    
    except ValueError as e:
        print("Invalid input, please correct vehicle details")
        return get_vehicle_input()


def add_package_cost_time(**kwargs):
    """
    To add package delivery cost and time to
    corresponding package details
    
    :param kwargs:
    package_details - list of package details as list of dict
    package_combo - list of packge details as possible combo satisfying the condition
    current_time - current time
    max_speed - maximum speed of vehicle
    base_delivery_cost - base delivery cost
    
    :return pack_cost_time: package details with corresponding time and cost added
    :rtype pack_cost_time: list of dict
    """
    pack_cost_time = []
    for package in kwargs['package_details']:
        for pack in kwargs['package_combo']:
            if package['package_id'] == pack['package_id']:
                pack_time = kwargs['current_time'] + float("{:.2f}".format(package['distance'] / kwargs['max_speed']))
                pack_cost = utils.get_package_delivery_cost(package, int(kwargs['base_delivery_cost']))
                pack_discount = utils.calculate_discount(package, pack_cost)
                pack_cost_time.append({'pack_id': package['package_id'], 'discount': pack_discount,
                                       'total_cost': pack_cost - pack_discount, 'time': pack_time})
    
    return pack_cost_time


def calculate_time_cost(**kwargs):
    """
    Function to calculate delivery time
    and cost of list of packages
    
    :param kwargs:
    base_delivery_cost - base delivery cost
    no_of_packages - number of packages
    package_details - list of package details as list of dict
    vehicle_details - vehicle details
    :type kwargs: list of dict
    
    :return package_cost_time: package details with corresponding time and cost added
    :rtype package_cost_time: list of dict
    
    """
    total_vehicle_available, max_speed, max_weight = [int(x) for x in kwargs['vehicle_details'].split(' ')]
    current_time = 0.0
    vehicle_available = total_vehicle_available
    vehicle_next_avail_time = []
    
    # sorting package in ascending order according to weight
    package_details_asc = utils.sort_package(kwargs['package_details'], "weight")
    
    package_cost_time = []
    
    while len(package_details_asc) > 0:
        package_combo = ()
        if vehicle_available > 0:
            # identifying the best possible combination of packages
            package_combo = utils.estimated_combo(package_details_asc, max_weight)
            if len(package_combo) > 0:
                package_details_asc = [x for x in package_details_asc if x not in package_combo]
                if len(package_details_asc) > 0:
                    # finding the time taken by vehicle to deliver and return back to delivery hub
                    estimated_delivery_time = float(
                        "{:.2f}".format(2 * utils.get_package_delivery_time(package_combo, max_speed)))
                    vehicle_next_avail_time.append(estimated_delivery_time + current_time)
                    package_cost_time += add_package_cost_time(package_details=kwargs['package_details'],
                                                               package_combo=package_combo,
                                                               current_time=current_time,
                                                               max_speed=max_speed,
                                                               base_delivery_cost=kwargs['base_delivery_cost'])
                    vehicle_available -= 1
                else:
                    package_cost_time += add_package_cost_time(package_details=kwargs['package_details'],
                                                               package_combo=package_combo,
                                                               current_time=current_time,
                                                               max_speed=max_speed,
                                                               base_delivery_cost=kwargs['base_delivery_cost'])
            else:
                break
        else:
            current_time = min(vehicle_next_avail_time)
            vehicle_available += 1
            vehicle_next_avail_time.remove(current_time)
    
    return package_cost_time


def display_delivery_time_cost(package_cost_time):
    """
    To print cost and time for list of all packages
    
    :param package_cost_time: package details with corresponding time and cost for delivery
    :type package_cost_time: list of dict
    
    :return:
    """
    print("Package id, discount, total cost, delivery time")
    for package in package_cost_time:
        print(package['pack_id'], package['discount'], package['total_cost'], package['time'])


def calculate_cost_time():
    """
    To calculate get package and vehicle details and
    call calculate delivery cost and time function
    
    :param:
    
    :return:
    """
    base_delivery_cost, no_of_packages, package_details = utils.get_package_input()
    
    vehicle_details = get_vehicle_input()
    
    package_cost_time = calculate_time_cost(base_delivery_cost=base_delivery_cost,
                                            no_of_packages=no_of_packages,
                                            package_details=utils.convert_package_details(package_details),
                                            vehicle_details=vehicle_details)
    
    display_delivery_time_cost(utils.sort_package(package_cost_time, "pack_id"))
    
    return package_cost_time
