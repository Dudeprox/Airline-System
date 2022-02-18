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
from typing import List
from customer import Customer
from flight import FlightSegment


# from time import sleep


class Filter:
    """ A class for filtering flight segments based on some criterion.

        This is an abstract class. Only subclasses should be instantiated.
    """

    def __init__(self) -> None:
        pass

    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data>, which match the
            filter specified in <filter_string>.

            The <filter_string> is provided by the user through the visual
            prompt, after selecting this filter.

            The <customers> is a list of all customers from the input dataset.

            If the filter has no effect or the <filter_string> is invalid then
            return the same flights segments from the <data> input.

            Precondition:
                - <customers> contains the list of all customers from the input
                  dataset
                - all flight segments included in <data> are valid segments
                  from the input dataset
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu
        """
        raise NotImplementedError


class ResetFilter(Filter):
    """ A class for resetting all previously applied filters, if any. """

    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Reset all of the applied filters. Returns a List containing all the
            flight segments corresponding to all trips of <customers>.

            The <data>, <customers>, and <filter_string> arguments for this
            type of filter are ignored.
        """
        flights = []
        for customer in customers:
            for trip in customer.get_trips():
                for flight in trip.get_flight_segments():
                    flights.append(flight)

        # TODO
        return flights

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Reset all of the filters applied so far (if any)!"


class CustomerFilter(Filter):
    """ A class for selecting the flight segments for a given customer. """

    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> made or received
            by the customer with the id specified in <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            customer ID.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        # Check if customer id is valid
        c_ids = []
        for customer in customers:
            c_ids.append(customer.get_id())

        try:
            int(filter_string)
        except ValueError:
            return data

        if int(filter_string) in c_ids:
            # Getting the trips the Customer Has
            trips = []
            for customer in customers:
                if int(filter_string) == customer.get_id():
                    for trip in customer.get_trips():
                        if trip not in trips:
                            trips.append(trip)

            # Extracting flights from trips and checking if there are in data
            flights = []
            for trip in trips:
                for flight in trip.get_flight_segments():
                    if flight in data and flight not in flights:
                        flights.append(flight)
            return flights
        else:
            return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter events based on customer ID"


class DurationFilter(Filter):
    """ A class for selecting only the flight segments lasting either over or
        under a specified duration.
    """

    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> with a duration of
            under or over the time indicated in the <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains the following
            input format: either "Lxxxx" or "Gxxxx", indicating to filter
            flight segments less than xxxx or greater than xxxx minutes,
            respectively.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """

        if len(filter_string) == 5 and \
                (filter_string[0] == "L" or filter_string[0] == "G") \
                and len(filter_string[1:]) == 4 \
                and filter_string[1:].isdigit():

            if filter_string[0] == "L":
                flights = []
                value = int(filter_string[1:])
                for flight in data:
                    if int(flight.get_duration().hour * 60 + \
                           flight.get_duration().minute + \
                           flight.get_duration().second / 60) < value:
                        flights.append(flight)
                return flights

            else:
                value = int(filter_string[1:])
                flights = []
                for flight in data:
                    if int(flight.get_duration().hour * 60 + \
                           flight.get_duration().minute + \
                           flight.get_duration().second / 60) > value:
                        flights.append(flight)
                return flights
        else:
            return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu
        """
        return "Filter flight segments based on duration; " \
               "L#### returns flight segments less than specified length, " \
               "G#### for greater "


class LocationFilter(Filter):
    """ A class for selecting only the flight segments which took place within
        a specific area.
    """

    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data>, which took place
            within a location specified by the <filter_string> (the IATA
            departure or arrival airport code of the segment was
            <filter_string>).

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            3-string IATA airport code. In the event of an invalid string:
              1. return the original list <data>, and
              2. your code must not crash.
        """
        iata = []
        for flight in data:
            if flight.get_dep() not in iata:
                iata.append(flight.get_dep())
                if flight.get_arr() not in iata:
                    iata.append(flight.get_arr())

        if (filter_string[0] == "D" or filter_string[0] == "A") and \
                len(filter_string) == 4 and filter_string[1].isupper() \
                and filter_string[2].isupper() and filter_string[3].isupper() \
                and isinstance(filter_string, str) and \
                filter_string[1:] in iata:

            if filter_string[0] == "D":
                flights = []
                for flight in data:
                    if flight.get_dep() == filter_string[1:] and flight not in \
                            flights:
                        flights.append(flight)
                return flights

            else:
                flights = []
                for flight in data:
                    if flight.get_arr() == filter_string[1:] and flight not in \
                            flights:
                        flights.append(flight)
                return flights
        else:
            return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter flight segments based on an airport location;\n" \
               "DXXX returns flight segments that depart airport XXX,\n" \
               "AXXX returns flight segments that arrive at airport XXX\n"


class DateFilter(Filter):
    """ A class for selecting all flight segments that departed and arrive
    between two dates (i.e. "YYYY-MM-DD/YYYY-MM-DD" or "YYYY MM DD YYYY MM DD").
    """

    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> that have departed
            and arrived between the range of two dates indicated in the
            <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains the following
            input format: either "YYYY-MM-DD/YYYY-MM-DD" or
            "YYYY MM DD YYYY MM DD", indicating to filter flight segments
            between the first occurrence of YYYY-MM-DD and the second occurence
            of YYYY-MM-DD.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        filter_slash = False
        filter_space = False

        # if filter_string[10] == "/" and "-" in filter_string:  # Check if this
        #     # "YYYY-MM-DD/YYYY-MM-DD" is the format

        try:
            datetime.datetime.strptime(filter_string[0:10], '%Y-%m-%d')
            datetime.datetime.strptime(filter_string[11:], '%Y-%m-%d')  #
            # Checks if the format works
            filter_slash = True and filter_string[10] == "/"
        except ValueError:
            filter_slash = False

        # elif filter_string.count(" ") == 5:  # check if this "YYYY MM DD YYYY
        #     # MM DD" is the format
        try:  # Checks if the format works
            datetime.datetime.strptime(filter_string[0:10], '%Y %m %d')
            datetime.datetime.strptime(filter_string[11:], '%Y %m %d')
            filter_space = True and filter_string[10] == " "
        except ValueError:
            filter_space = False

        if filter_slash is False and filter_space is False:
            return data
        else:
            if filter_slash is True:
                d1 = datetime.datetime.strptime(filter_string[0:10],
                                                '%Y-%m-%d').date()
                d2 = datetime.datetime.strptime(filter_string[11:],
                                                '%Y-%m-%d').date()
                flights = []
                for flight in data:
                    if (d1 <= flight.get_times()[0].date() <= d2) and \
                            (d1 <= flight.get_times()[1].date() <= d2):
                        # or (d2 <= flight.get_times()[0].date() <= d1
                        #     and d2 <= flight.get_times()[1].date() <= d1):

                        flights.append(flight)
                return flights

            else:
                d1 = datetime.datetime.strptime(filter_string[0:10],
                                                '%Y %m %d').date()
                d2 = datetime.datetime.strptime(filter_string[11:],
                                                '%Y %m %d').date()
                flights = []
                for flight in data:
                    if (d1 <= flight.get_times()[0].date() <= d2) \
                            and (d1 <= flight.get_times()[1].date() <= d2):
                        flights.append(flight)
                return flights

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter flight segments based on dates; " \
               "'YYYY-MM-DD/YYYY-MM-DD' or 'YYYY-MM-DD,YYYY-MM-DD'"


class TripFilter(Filter):
    """ A class for selecting the flight segments for a trip. """

    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> where the
            <filter_string> specified the trip's reservation id.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            Reservation ID.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        # Make trips ids to check if filter string is valid
        trip_ids = []
        for customer in customers:
            for trip in customer.get_trips():
                trip_ids.append(trip.reservation_id)

        if filter_string in trip_ids:  # Checking for validity of the filter
            # Getting all the trips that exist
            trips = []
            for customer in customers:
                for trip in customer.get_trips():
                    trips.append(trip)
            # Check if any of the trip's id match given id
            new_trips = []
            for trip in trips:
                if trip.reservation_id == filter_string:
                    new_trips.append(trip)
            # Check if flights in matched trips are in data and then append
            flights = []
            for trip in new_trips:  # Matched Trips
                for flight in trip.get_flight_segments():
                    if flight in data and flight not in flights:
                        flights.append(flight)
            return flights

        else:
            return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter events based on a reservation ID"


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'doctest',
            'customer', 'flight', 'time'
        ],
        'max-nested-blocks': 5,
        'allowed-io': ['apply', '__str__']
    })
