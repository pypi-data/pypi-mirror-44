"""Module for connecting to Ip2Location DB"""
from ip2geotools.databases.noncommercial import Ip2Location
from ip2geotools.errors import (LocationError, IpAddressNotFoundError, PermissionRequiredError,
                                InvalidRequestError, InvalidResponseError, ServiceError,
                                LimitExceededError)

from ip2geotools_locator.folium_map import FoliumMap
from ip2geotools_locator.utils import Location, LOGGER as logger


class Ip2LocationDB:
    """
    Class for handling DB connection into Ip2location Database
    """
    # Instance of map for placing markers
    m = FoliumMap()
    __db_data = None

    def __init__(self, file_path):
        # This database needs DB file to read data
        if file_path is None:
            logger.critical("Database %s needs DB file!", Ip2Location.__name__)
        self.__file_path = file_path

    def get_location(self, ip_address):
        """
        Retrieves location for given IP address from Ip2location database
        Validation and exception handling included.
        """
        try:
            # Try to get and return location
            self.__db_data = Ip2Location.get(ip_address, None, self.__file_path)
            if self.__db_data.latitude is None or self.__db_data.longitude is None:
                raise InvalidResponseError
            logger.info("DB returned location %.3f N, %.3f E", self.__db_data.latitude,
                        self.__db_data.longitude)

            return Location(self.__db_data.latitude, self.__db_data.longitude)

        except IpAddressNotFoundError as exception:
            # Handling for IpAddressNotFoundError exception
            logger.warning("Database could not find IP address. IpAddressNotFoundError: %s ",
                           str(exception))

        except PermissionRequiredError as exception:
            # Handling for PermissionRequiredError exception
            logger.critical("Additional setings required for DB. PermissionRequiredError: %s ",
                            str(exception))

        except ServiceError as exception:
            # Handling for ServiceError exception
            logger.error("Service is unavailable. ServiceError: %s ", str(exception))

        except LimitExceededError as exception:
            # Handling for LimitExceededError exception
            logger.warning("LimitExceededError: %s ", str(exception))

        except (LocationError, InvalidRequestError, InvalidResponseError) as exception:
            # Handling for invalid data, request and response exception
            logger.error("returned %s ", str(exception.__class__))

        except TypeError as exception:
            # Handling for TypeError exception (in case of database returning None values)
            logger.warning("DB returned invalid values. TypeError: %s ", str(exception))

    def add_to_map(self):
        """
        Add Folium Marker to map
        Call get_location(ip) method before adding any markers to map
        """
        try:
            logger.debug("Calling add_marker method for %s DB", Ip2Location.__name__)
            self.m.add_marker_noncommercial(Ip2Location.__name__,
                                            self.__db_data.ip_address,
                                            self.__db_data.country,
                                            self.__db_data.region,
                                            self.__db_data.city,
                                            self.__db_data.latitude,
                                            self.__db_data.longitude)
        except AttributeError as exception:
            # Handling for AttributeError exception (in case of database returning None values)
            logger.warning("Cannot add empty marker %s ", str(exception))
