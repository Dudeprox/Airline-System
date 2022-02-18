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
from __future__ import annotations
from typing import Dict, List, Optional, Tuple
import datetime

# Global Airplane Seat Type capacity
AIRPLANE_CAPACITY = {"Economy": 150, "Business": 22}


class FlightSegment:
    """ A FlightSegment offered by the airline system.

    === Public Attributes ===
    seat_capacity:
        the class of seat and total number of seats available on a specific
        segment.
    seat_availability:
        the class of seat and number of seats still available on a specific
        segment.

    === Representation Invariants ===
        -  the keys in seat_availability.keys() must all be >= 0
           (i.e. they cannot be negative)
    """

    # === Private Attributes ===
    # _flight_id:
    #     a unique identifier for this flight.
    # _time:
    #     a tuple containing the departure and arrival time of a segment.
    # _manifest:
    #      a list of tuples containing all customers' ID and type of flight
    #      class that they've taken (e.g. economy).
    # _base_fare_cost:
    #     the base cost of the fare (e.g., $0.1225/km).
    # _flight_duration:
    #     the total time it takes for the flight segment to complete.
    # _flight_length:
    #     the number of kilometres between the departure and arrival locations.
    # _dep_loc:
    #     the unique 3-digit (IATA) airport identifier of where the flight
    #     segment is departing (i.e. leaving from).
    # _arr_loc:
    #     the unique 3-digit (IATA) airport identifier of where the flight
    #     segment is landing (i.e. arriving to).
    # _long_lat:
    #     a tuple of tuples, containing the longitude and latitude of the
    #     departure and arrival destinations.
    #
    # === Representation Invariants ===
    #     -  _flight_length >= 0
    #     -  _dep_loc and _arr_loc must be exactly three characters [A-Z]
    #        and are assumed to be valid and distinct IATA airport codes.

    seat_capacity: Dict[str, int]  # str: class, int: seats_available
    seat_availability: Dict[str, int]  # str: class, int: seats_available
    _flight_id: str
    _time: Tuple[datetime.datetime, datetime.datetime]
    _base_fare_cost: float
    _flight_duration: datetime.time
    _flight_length: float
    _dep_loc: str
    _arr_loc: str
    _long_lat: Tuple[Tuple[float, float], Tuple[float, float]]
    _manifest: List[Tuple[int, str]]  # (customer_id, seat_type)

    def __init__(self, fid: str, dep: datetime.datetime, arr: datetime.datetime,
                 base_cost: float, length: float, dep_loc: str, arr_loc: str,
                 long_lat: Tuple[Tuple[float, float],
                                 Tuple[float, float]]) -> None:
        """ Initialize a FlightSegment object based on the parameters specified.
        """

        self.seat_availability = {"Economy": 150, "Business": 22}  #
        self.seat_capacity = {"Economy": 150, "Business": 22}  #
        self._manifest = []  #
        self._long_lat = long_lat
        self._arr_loc = arr_loc
        self._dep_loc = dep_loc
        self._flight_length = length
        self._base_fare_cost = base_cost
        self._flight_id = fid
        self._time = (dep, arr)

        # duration = datetime.datetime.combine(datetime.datetime.min,
        # arr.time())\ - datetime.datetime.combine(datetime.datetime.min,
        # dep.time()) time = (datetime.datetime.min + duration).time() s =
        # str(arr - dep) s = s.split(':') self._flight_duration =
        # datetime.time(int(s[0]), int(s[1]))

        self._flight_duration = datetime.time(0)

        # TODO

    def __repr__(self) -> str:
        return ("[" + str(self._flight_id) + "]:" + str(self._dep_loc) + "->" +
                str(self._arr_loc))

    def get_length(self) -> float:
        """ Returns the length, in KMs, of this flight segment. """
        return self._flight_length
        # TODO

    def get_times(self) -> Tuple[datetime.datetime, datetime.datetime]:
        """ Returns the (departure, arrival) time of this flight segment. """
        return self._time
        # TODO

    def get_arr(self) -> str:
        """ Returns the arrival airport (i.e. the IATA). """
        return self._arr_loc
        # TODO

    def get_dep(self) -> str:
        """ Returns the departure airport (i.e. the IATA). """
        return self._dep_loc
        # TODO

    def get_fid(self) -> str:
        """ Returns the flight identifier. """
        return self._flight_id
        # TODO

    def get_long_lat(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """ Returns the longitude and latitude of a FlightSegment,
            specifically like this: ((LON1, LAT1), (LON2, LAT2)).
        """
        return self._long_lat
        # TODO

    def get_duration(self) -> datetime.time:
        """ Returns the duration of the flight. """
        # diff = self._time[1] - self._time[0]
        # self._flight_duration = datetime.time(diff.seconds)
        # return self._flight_duration
        # diff = self._time[1].date() - self._time[0].date()

        # duration = datetime.datetime.combine(datetime.datetime.today(),
        #                                      self._time[1].time()) - \
        #            datetime.datetime.combine(datetime.datetime.today(),
        #                                      self._time[0].time())

        # s = str(arr - dep)
        # s = s.split(':')
        # self._flight_duration = datetime.time(int(s[0]), int(s[1]))

        duration = datetime.datetime.combine \
                       (datetime.datetime.min, self._time[1].time()) \
                   - datetime.datetime.combine(datetime.datetime.min,
                                               self._time[0].time())

        time = (datetime.datetime.min + duration).time()
        self._flight_duration = time

        return time

        # TODO

    def get_base_fare_cost(self) -> float:
        """ Returns the base fare cost for this flight segment. """
        return self._base_fare_cost
        # TODO

    def check_manifest(self, cid: int) -> bool:
        """ Returns True if a certain customer <cid> has booked a seat
            on this specific flight, otherwise False.
        """
        # _manifest: List[Tuple[int, str]]  # (customer_id, seat_type)
        for item in self._manifest:
            if item[0] == cid:
                return True
        return False
        # TODO

    def check_seat_class(self, cid: int) -> Optional[str]:
        """ Checks the manifest to see what class of cabin a certain customer
            (based on their <cid>) has booked. None is returned in the event
            there is no seat booked for that <cid>.
        """
        # _manifest: List[Tuple[int, str]]  # (customer_id, seat_type)
        for item in self._manifest:
            if item[0] == cid:
                return item[1]
        return None

        # TODO

    def book_seat(self, cid: int, seat_type: str) -> None:
        """ Book a seat of the given <seat_type> for the customer <cid>.
            If that customer is already booked, do nothing. If the seat
            type is different, and it is available, make the change.
        """
        # _manifest: List[Tuple[int, str]]  # (customer_id, seat_type)
        flag = False
        for item in self._manifest:

            if item == (cid, seat_type):  # cid & seat is there.
                return None

            elif item[0] == cid and item[1] != seat_type:
                # Customer is there but seat is different
                if 0 < self.seat_availability[seat_type] <= self.seat_capacity \
                        [seat_type]:  # If the seat is available

                    self.seat_availability[item[1]] += 1
                    # Give Orignal One Point
                    self.seat_availability[seat_type] -= 1  # Give new one less

                    new_item = list(item)
                    new_item[1] = seat_type
                    new = (int(new_item[0]), str(new_item[1]))
                    self._manifest.append(new)

                    flag = True
                    return None

                elif self.seat_availability[seat_type] == 0:
                    # if the seat type is not available
                    return None
                else:
                    return None

        if flag is False:  # If customer and seat is not in manifeast
            self._manifest.append((cid, seat_type))
            self.seat_availability[seat_type] -= 1
            return None
        else:
            return None

        # TODO

    def cancel_seat(self, cid: int) -> None:
        """	If a seat has already been booked by <cid>, cancel the booking
            and restore the seat's availability. Otherwise, do nothing and
            return None.
        """
        # Check if the customer hasn't booked anything
        count = 0
        for item in self._manifest:
            if item[0] != cid:
                count += 1

        if len(self._manifest) == count:
            return None
        else:
            # If there is a seat booking cancel it
            l = []
            for item in self._manifest:
                if item[0] == cid:
                    seat = item[1]
                    self.seat_availability[seat] += 1
                    l.append(item)

            for i in l:
                self._manifest.remove(i)

            return None

        # TODO


# ------------------------------------------------------------------------------
class Trip:
    """ A Trip is composed of FlightSegment(s) which makes up a customer's
        itinerary.

    === Public Attributes ===
    reservation_id:
         a unique identifier for this trip.
    customer_id:
         the unique identifier of the customer who booked this trip.
    trip_departure:
         the date in which this trip was booked.
    """
    # === Private Attributes ===
    # _flights:
    #      a list of all flight segments for this particular trip
    reservation_id: str
    customer_id: int
    trip_departure: datetime.date
    _flights: List[FlightSegment]

    def __init__(self, rid: str, cid: int, trip_date: datetime.date,
                 flight_segments: List[FlightSegment]) -> None:
        """ Initializes a trip object given the specified parameters. """
        self.reservation_id = rid
        self.customer_id = cid
        self.trip_departure = trip_date
        self._flights = flight_segments

        # TODO

    def get_flight_segments(self) -> List[FlightSegment]:
        """ Returns a list of all Flight Segments part of this booking. """
        return self._flights
        # TODO

    def get_reservation_id(self) -> str:
        """ Returns this Trip's Reservation ID. """
        return self.reservation_id
        # TODO

    def get_in_flight_time(self) -> int:
        """ Returns the amount of time (in minutes) the trip is spent in
            flight (i.e. the time in the air only).
        """
        acc = 0
        for item in self._flights:
            acc += item.get_duration().hour * 60 + \
                   item.get_duration().minute + item.get_duration().second / 60
        return acc
        # TODO

    def get_total_trip_time(self) -> int:
        """ Returns the amount of time (in minutes) the trip is takes,
            including all transit time (i.e. including waiting for the next
            flight on a layover).
        """
        # From First Flight to last Flight

        dep = []
        arr = []
        for flight in self._flights:
            dep.append(flight.get_times()[0])
            arr.append(flight.get_times()[1])

        begin = min(dep)
        end = max(arr)

        duration = datetime.datetime.combine \
                       (datetime.datetime.min, end.time()) \
                   - datetime.datetime.combine(datetime.datetime.min,
                                               begin.time())

        time = (datetime.datetime.min + duration).time()

        m = time.get_duration().hour * 60 + time.get_duration().minute + \
            time.get_duration().second / 60

        return int(m)

        # TODO


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'doctest',
            'datetime', '__future__'
        ],
        'max-attributes': 11,
        'max-args': 9
    })
