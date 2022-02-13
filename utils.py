from itertools import combinations, chain
import json


def get_offer_coupon():
    """
    To get details of available offer coupons
    :return offer_coupons:
    :rtype offer_coupons
    """
    f = open('offer_coupons.json')
    offer_coupons = json.load(f)
    f.close()
    return offer_coupons


def validate_input(input_details, input_count):
    """
    To get user input details and validate if all details are present
    
    :param input_details: user input as string
    :type input_details: list of string
    
    :param input_count: number of inputs to be present in the input string
    :type input_count: int
    
    :return:
    """
    
    for input_value in input_details:
        if len(str(input_value).split(" ")) != int(input_count):
            raise ValueError


def get_package_input():
    """
    To get package details from user
    
    :param:
    
    :returns base_delivery_cost, no_of_packages, package_details:
    :rtype base_delivery_cost: basestring
    :rtype no_of_packages: basestring
    :rtype package_details: basestring
    """
    try:
        print("Please enter base delivery cost and no of packages : ")
        # will raise exception if 2 inputs with comma separation is not present
        base_delivery_cost, no_of_packages = input().split(" ")

        print("Please enter package id, package weight, " +
              "distance(km) and coupon code : ")

        package_details = [input() for i in range(int(no_of_packages))]
        
        validate_input(package_details, 4)
        
    except ValueError as e:
        print("Invalid input please correct the input and try again")
        return get_package_input()
    
    return base_delivery_cost, no_of_packages, package_details


def evaluate_condition(value, criteria):
    """
    Function to check if the provided value satisfies the condition
    
    :param value: value to check if it satisfies the condition
    :type value: basestring
    
    :param criteria: Condition to be verified
    :type criteria: basestring
    
    :return condition: the condition to be verified as string
    :rtype condition: basestring
    """
    try:
        condition = int(value) in range(int(criteria.split('-')[0]), int(criteria.split('-')[1])+1) \
            if '-' in criteria \
            else eval(str(value)+criteria)
    except Exception as e:
        print("Execution failed with Execption ",e)
    else:
        return condition


def calculate_discount(package_detail, delivery_cost):
    """
    To validate if the package is applicable for discount
    and calculate discount based on coupon code
    
    :param package_detail: package details
    :type package_detail: dict
    :param delivery_cost delivery cost of package
    :type delivery_cost: int
    
    :return discount_amount: details of package with corresponding discount amount
    :rtype discount_amount: list of string
    """
    discount_amount = 0
    offer_coupon = get_offer_coupon()
    if package_detail['coupon_code'] in offer_coupon:
        coupon_details = offer_coupon[package_detail['coupon_code']]

        if evaluate_condition(package_detail['distance'], coupon_details['distance']) \
                and evaluate_condition(package_detail['weight'], coupon_details['weight']):
            discount_amount = int(delivery_cost*int(coupon_details['discount'])/100)
    
    return discount_amount


def get_package_delivery_cost(package_detail, base_delivery_cost):
    """
    Logic to calculate delivery cost of package
    
    :param package_detail: package details with coupon code
    :type package_detail: dict
    :param base_delivery_cost: base delivery cost of package
    :type base_delivery_cost: int
    
    :return delivery_cost:
    :rtype delivery_cost:
    """
    delivery_cost = int(base_delivery_cost) + int(package_detail['weight']) * 10 \
                    + int(package_detail['distance']) * 5
    
    return delivery_cost


def sort_package(dict_array, sort_key):
    """
    Sort list of dict based on the key provided
    
    :param dict_array: list of dict to be sorted
    :type dict_array: list of dict
    
    :param sort_key: Key which is to be used to sort
    :type sort_key: basestring
    
    :return: sorted list of dict
    :rtype: list of dict
    """
    try:
        return sorted(dict_array, key=lambda i: i[sort_key])
    except KeyError as e:
        print("Execution failed with error", e)


def convert_package_details(package_details):
    """
    Convert package details from string to dict
    
    :param package_details: Package details as string
    :type package_details: list
    
    :return: package details as dict
    :rtype: list of dict
    """
    try:
        return [{"package_id": package_detail.split()[0], "weight": int(package_detail.split()[1]),
                 "distance": int(package_detail.split()[2]), "coupon_code": package_detail.split()[3]}
                for package_detail in package_details]
    except IndexError as e:
        print("Execution failed with error", e)


def estimated_combo(package_details, max_weight):
    """
    This function loops through all possible combinations
    and returns the combination which satisfies below condition
    1. weight should be less than max_weight and should be max
    when compared to other combinations
    2. if two combination have same weight the precedence
    will be for the one with max number of packages
    
    :param package_details: Package details as string
    :type package_details: list
    
    :param max_weight: Maximum weight a vehicle can accommodate
    :type max_weight: int
    
    :return final_combination: list of possible package combination that satisfies the condition
    :rtype final_combination: list of dict
    """
    final_combination = ()
    allCombinations = chain(*(combinations(package_details, i) for i in range(len(package_details) + 1)))
    
    final_combination = ()
    final_combination_weight = 0
    for combi in allCombinations:
        combination_weight = sum(package['weight'] for package in combi)
        if final_combination_weight < combination_weight <= max_weight \
                or (len(final_combination) < len(combi) and final_combination_weight == combination_weight):
            final_combination_weight = combination_weight
            final_combination = combi
    
    return final_combination


def get_package_delivery_time(package_details, max_speed):
    """
    This function calculates delivery time based on vehicle speed
    
    :param package_details: list of packages
    :type package_details: list of dict
    
    :param max_speed: maximum speed of vehicle
    :type max_speed: int
    
    :return: list of packages with corresponding delivery time
    :rtype: list of dict
    """
    
    return max([package_detail['distance']/max_speed for package_detail in package_details])
