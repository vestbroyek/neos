"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str, parse_y_n_bool
from datetime import datetime


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, designation: str, name: str = None, diameter: float = float('nan'), hazardous: str = None, approaches: list = [], **info):
        """Create a new `NearEarthObject`.
        :param designation:     The NEO's primary designation (pdes) e.g. 433
        :param name:            The NEO's name, e.g. Eros. Not always available.
        :param diameter:        The NEO's diameter in km 
        :param hazardous:       Whether the NEO was potentially hazardous (pha)
        :param approaches:      A list of the NEO's approaches 
        :param info:            A dictionary of excess keyword arguments supplied to the constructor.
        """
        # TODO: coerce these values to their appropriate data type and handle any edge cases, 
        # such as a empty name being represented by `None`
        self.designation = str(designation)
        self.name = name if name is not None else None
        self.diameter = float('nan') if diameter == '' else float(diameter)
        self.hazardous = parse_y_n_bool(hazardous) if hazardous is not None else None # there are also some missing values here 

        # Create an empty initial collection of linked approaches.
        self.approaches = approaches

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # TODO: Use self.designation and self.name to build a fullname for this object.
        if self.name: # if name is not none, return it alongside the designation, like 433 Eros
            return self.designation + " " + self.name
        else: # otherwise just use designation
            return self.designation

    def __str__(self):
        """Return `str(self)`."""
        if not self.hazardous:
            hazardous = "not hazardous"
        else:
            hazardous = "hazardous"
        return f"{self.fullname}, which has a diameter of {self.diameter:.3f} and is {hazardous}"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, time: datetime, distance: float, velocity: float, neo: NearEarthObject = None, **info):
        """Create a new `CloseApproach`.

        :param time:        The time of the close approach
        :param distance:    The distance in AU of the approach from earth
        :param velocity:    The speed at which the NEO passed in km/s
        :param neo:         A NEO that made a close approach
        :param info:        A dictionary of excess keyword arguments supplied to the constructor.
        """
        # TODO: coerce these values to their appropriate data type and handle any edge cases.
        self._designation = neo.fullname if neo is not None else None
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"{self._designation} passed Earth at {self.time_str}, at a distance of {self.distance} au and velocity of {self.velocity} km/s"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
