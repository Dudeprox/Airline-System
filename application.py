"""
UTM:CSC148, Winter 2020
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Bogdan Simion, Michael Liut, Paul Vrbik
"""
import datetime
import csv
from typing import Dict, List, Tuple, Optional
from airport import Airport
from customer import Customer
from flight import Trip, FlightSegment
from visualizer import Visualizer

#############################################
# DO NOT DECLARE ANY OTHER GLOBAL VARIABLES!
#############################################

# AIRPORT_LOCATIONS: global mapping of an airport's IATA with their respective
#                    longitude and latitude positions.
# NOTE: This is used for our testing purposes, so it has to be populated in
# create_airports(), but you are welcome to use it as you see fit.
AIRPORT_LOCATIONS = {}

# DEFAULT_BASE_COST: Default rate per km for the base cost of a flight segment.
DEFAULT_BASE_COST = 0.1225


def import_data(file_airports: str, file_customers: str, file_segments: str,
                file_trips: str) -> Tuple[List[List[str]], List[List[str]],
                                          List[List[str]], List[List[str]]]:
    """ Opens all the data files <data/filename.csv> which stores the CSV data,
        and returns a tuple of lists of lists of strings. This contains the read
        in data, line-by-line, (airports, customers, flights, trips).

        Precondition: the dataset file must be in CSV format.
    """

    airport_log, customer_log, flight_log, trip_log = [], [], [], []

    airport_data = csv.reader(open(file_airports))
    customer_data = csv.reader(open(file_customers))
    flight_data = csv.reader(open(file_segments))
    trip_data = csv.reader(open(file_trips))

    for row in airport_data:
        airport_log.append(row)

    for row in flight_data:
        flight_log.append(row)

    for row in customer_data:
        customer_log.append(row)

    for row in trip_data:
        trip_log.append(row)

    return airport_log, flight_log, customer_log, trip_log


def create_customers(log: List[List[str]]) -> Dict[int, Customer]:
    """ Returns a dictionary of Customer IDs and their Customer instances, based
    on the customers from the input dataset from the <log>.

    Precondition:
        - The <log> list contains the input data in the correct format.
    """
    dic = {}
    for customer_attributes in log:
        id_ = int(customer_attributes[0])
        name = str(customer_attributes[1])
        age = int(customer_attributes[2])
        nat = str(customer_attributes[3])
        new_customer = Customer(id_, name, age, nat)
        dic.setdefault(int(customer_attributes[0]), new_customer)

    return dic
    # TODO


def create_flight_segments(log: List[List[str]]) \
        -> Dict[datetime.date, List[FlightSegment]]:
    """ Returns a dictionary storing all FlightSegments, indexed by their
    departure date, based on the input dataset stored in the <log>.

    Precondition:
    - The <log> list contains the input data in the correct format.
    """
    # long_lat: Tuple[Tuple[float, float],Tuple[float, float]]
    # _long_lat:
    #     a tuple of tuples, containing the longitude and latitude of the
    #     departure and arrival destinations.
    # DEFAULT_BASE_COST
    dic = {}

    for flight_attributes in log:
        dep = datetime.datetime.strptime(flight_attributes[3]
                                         + " " + flight_attributes[4],
                                         '%Y:%m:%d %H:%M')
        if dep.date() not in dic:
            dic[dep.date()] = []
    l = []
    for flight_attributes in log:
        flight_id = str(flight_attributes[0])

        dep_loc = str(flight_attributes[1])

        arr_loc = str(flight_attributes[2])

        dep = datetime.datetime.strptime(flight_attributes[3]
                                         + " " + flight_attributes[4],
                                         '%Y:%m:%d %H:%M')

        arr = datetime.datetime.strptime(flight_attributes[3] +
                                         " " + flight_attributes[5],
                                         '%Y:%m:%d %H:%M')

        length = float(flight_attributes[6])

        long_lat = (AIRPORT_LOCATIONS[dep_loc], AIRPORT_LOCATIONS[arr_loc])

        flight_segment = FlightSegment(flight_id, dep, arr,
                                       DEFAULT_BASE_COST, length, dep_loc,
                                       arr_loc, long_lat)

        l.append(flight_segment)
        # dic[dep.date()].append(flight_segment)

    for flight in l:
        key = flight.get_times()[0].date()
        if key in dic and flight not in dic[key]:
            dic[key].append(flight)

    return dic

    # TODO


def create_airports(log: List[List[str]]) -> List[Airport]:
    """ Return a list of Airports with all applicable data, based
    on the input dataset stored in the <log>.

    Precondition:
    - The <log> list contains the input data in the correct format.
    """
    l = []
    for airport_attributes in log:
        id_ = str(airport_attributes[0])
        name = str(airport_attributes[1])
        location = (float(airport_attributes[2]), float(airport_attributes[3]))
        new_airport = Airport(id_, name, location)
        if new_airport not in l:
            l.append(new_airport)

    for airport in l:
        i = airport.get_airport_id()
        loc = airport.get_location()
        AIRPORT_LOCATIONS.setdefault(i, loc)

    return l


# def parser(l: List[str]) -> List[List[str]]:
#     new = []
#     for item in l:
#         if "[" in item or "(" in item or ")" in item:
#             item = item.replace("[", "")
#             item = item.replace("(", "")
#             item = item.replace(")", "")
#             item = item.replace("'", "")
#         new.append(item)
#     new[-1] = " "
#     date = datetime.datetime.strptime(str(new[2]), '%Y-%m-%d').date()
#     trip_date = datetime.datetime.strptime(str(new[2]), '%Y-%m-%d').date()
#     o = []
#     acc = [l[0], int(l[1]), date]
#     for i in range(3, len(new)):
#         o.append(new[i])
#     acc.append(o)
#
#     return acc


def get_min(l: List[FlightSegment]) -> Optional:
    """
    Gets the earliest flight out of a list of flightsegments
    """
    # Appends all dates of flights
    dates = []
    for flight in l:
        dep = flight.get_times()[0].time()
        dates.append(dep)

    m = min(dates)

    # Returns the earliest departed flights
    for flight in l:
        if flight.get_times()[0].time() == m:
            return flight

    return None


def h_m_1(f_s: List[FlightSegment], acc: Optional) \
        -> List[Tuple[FlightSegment, str]]:
    """
    Returns a list of two element tuples with a Flightsegment as and item and
    its seat type.
    """

    trip_list_u_seat = []

    for flight in f_s:
        trip_list_u_seat.append(
            (flight, flight.check_seat_class(int(acc[1]))))

    return trip_list_u_seat


def load_trips(log: List[List[str]], customer_dict: Dict[int, Customer],
               flight_segments: Dict[datetime.date, List[FlightSegment]]) \
        -> List[Trip]:
    """ Creates the Trip objects and makes the bookings.

    Preconditions:
    - The <log> list contains the input data in the correct format.
    - the customers are already correctly stored in the <customer_dict>,
    indexed by their customer ID.
    - the flight segments are already correctly stored in the <flight_segments>,
    indexed by their departure date
    """
    trips_acc = []
    # Make the Trip and do the booking for the customer
    for l in log:
        new = []
        for item in l:
            if "[" in item or "(" in item or ")" in item:
                item = item.replace("[", "").replace("(", "") \
                    .replace(")", "").replace("'", "").replace("]", " ")

                # item = item.replace("(", "")
                # item = item.replace(")", "")
                # item = item.replace("'", "")

            new.append(item)
        # print(new)
        # date = datetime.datetime.strptime(str(new[2]), '%Y-%m-%d').date()
        # trip_date = datetime.datetime.strptime(str(new[2]), '%Y-%m-%d').date()
        # o = []
        acc = [l[0], int(l[1]), datetime.datetime.strptime \
            (str(new[2]), '%Y-%m-%d').date(), []]
        for i in range(3, len(new)):
            acc[3].append(new[i])
        # acc.append(acc[3])
        # print(acc)

        # print(acc)
        # __________________________________________________________________

        # reservation_id = acc[0]
        # customer_id = int(acc[1])
        # customer = customer_dict[int(acc[1])]
        # itinerary = acc[3]

        fs = []
        for i in range(0, len(acc[3]), 2):
            if acc[3][i + 1] != " ":  # If it connects
                # dep_loc = acc[3][i]
                # seat = acc[3][i + 1]
                # arr_loc = acc[3][i + 2]
                fs.append([acc[3][i], acc[3][i + 1], acc[3][i + 2]])

        # print(fs)

        # f_s = flights(fs, date, flight_segments, customer_id)

        # _____________________________________________________________________
        # Gets the Earliest Flight on that Departure Date
        # _____________________________________________________________________

        # c_one = 0
        f_segments = []  # First Avaiable Flights avaiable
        if datetime.datetime.strptime(str(new[2]),
                                      '%Y-%m-%d').date() in flight_segments:
            for flight in flight_segments \
                    [datetime.datetime.strptime(str(new[2]), '%Y-%m-%d') \
                        .date()]:
                if flight.get_dep() == fs[0][0] and \
                        flight.get_arr() == fs[0][2] \
                        and flight.seat_availability[fs[0][1]] > 0:
                    # flight.book_seat(int(customer_id), fs[0][1]) ***
                    f_segments.append(flight)
                # else:  # If there is no flight that leaves that day
                #     c_one += 1
            # if c_one == len(flight_segments[datetime.datetime.strptime(str(
            # new[2]), '%Y-%m-%d').date()]): continue
            if len(f_segments) == 0:
                continue

        else:  # if there is not date MOVE- ON
            continue

        f_s = []  # Contains the first flight of departing
        if len(f_segments) > 1:
            # f_min = get_min(f_segments)
            get_min(f_segments).book_seat(int(acc[1]), fs[0][1])
            f_s.append(get_min(f_segments))  # Get the first flight departing
        else:
            f_segments[0].book_seat(int(acc[1]), fs[0][1])
            f_s.append(f_segments[0])

        # _________________________________________________________________

        new_date = f_s[0].get_times()[1].date()

        for i in range(1, len(fs)):
            # dep_loc = fs[i][0]
            # seat = fs[i][1]
            # arr_loc = fs[i][2]

            while new_date not in flight_segments:  # if the
                new_date = new_date + datetime.timedelta(days=1)

            c = False
            # counter = 0
            while c is False:
                for flight in flight_segments[new_date]:  # For flight
                    if flight.get_dep() == fs[i][0] and flight.get_arr() \
                            == fs[i][2] \
                            and flight.seat_availability[fs[i][1]] > 0:
                        flight.book_seat(int(acc[1]), fs[i][1])
                        f_s.append(flight)
                        c = True
                    # else:
                    #     counter += 1

                # if counter == len(flight_segments[new_date]):
                #     new_date = new_date + datetime.timedelta(days=1)
                #     counter = 0
                if c is False:
                    new_date = new_date + datetime.timedelta(days=1)

        # new_trip = Trip(acc[0], int(acc[1]), date, f_s)
        trips_acc.append(Trip(acc[0], int(acc[1]),
                              datetime.datetime.strptime(str(new[2]),
                                                         '%Y-%m-%d').date(),
                              f_s))

        # trip_list_u_seat = []
        #
        # for flight in f_s:
        #     trip_list_u_seat.append(
        #         (flight, flight.check_seat_class(int(acc[1]))))

        # h_m_1(f_s, acc)

        customer_dict[int(acc[1])].book_trip(acc[0], h_m_1(f_s, acc),
                                             datetime.datetime.strptime(
                                                 str(new[2]),
                                                 '%Y-%m-%d').date())

    return trips_acc

    # TODO


if __name__ == '__main__':
    print("\n---------------------------------------------")
    print("Reading in all data! Processing...")
    print("---------------------------------------------\n")

    # input_data = import_data('data/airports.csv', 'data/customers.csv',
    #     'data/segments.csv', 'data/trips.csv')
    input_data = import_data('data/airports.csv', 'data/customers.csv',
                             'data/segments_small.csv', 'data/trips_small.csv')

    airports = create_airports(input_data[0])
    print("Airports Created! Still Processing...")
    flights = create_flight_segments(input_data[1])
    print("Flight Segments Created! Still Processing...")
    customers = create_customers(input_data[2])
    print("Customers Created! Still Processing...")
    print("Loading trips can take a while...")
    trips = load_trips(input_data[3], customers, flights)
    print("Trips Created! Opening Visualizer...\n")

    flights_len = 0
    for ky in flights:
        flights_len += len(flights[ky])

    print("---------------------------------------------")
    print("Some Statistics:")
    print("---------------------------------------------")
    print("Total airports in the dataset:", len(airports))
    print("Total flight segments in the dataset:", flights_len)
    print("Total customers in the dataset:", len(customers))
    print("Total trips in the dataset:", len(trips))
    print("---------------------------------------------\n")

    all_flights = [seg for tp in trips for seg in tp.get_flight_segments()]
    all_customers = [customers[cid] for cid in customers]

    V = Visualizer()
    V.draw(all_flights)

    while not V.has_quit():

        flights = V.handle_window_events(all_customers, all_flights)

        all_flights = []

        for flt in flights:
            all_flights.append(flt)

        V.draw(all_flights)

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'csv', 'datetime', 'doctest',
            'visualizer', 'customer', 'flight', 'airport'
        ],
        'max-nested-blocks': 6,
        'allowed-io': [
            'create_customers', 'create_airports', 'import_data',
            'create_flight_segments', 'load_trips'
        ],
        'generated-members': 'pygame.*'
    })
