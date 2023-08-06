from datetime import datetime
from LatLon import LatLon, Latitude, Longitude


class Agent():
    """
    Agents are located at ther *point*, which is a lat-lon coordinate pair.
    They move through their route, which is a series of points that
    connect their current location to their destination.
    """

    def __init__(self,
                 point,
                 dest,
                 router,
                 speed=3):
        """
        :param point: current location of agent
        :param dest: destination point of agent
        :param speed: speed in metres per second
        :param router: a router instance

        :type point: LatLon point
        :type dest: LatLon point
        :type speed: float
        :type router: NXRouter or BRouter instance
        """

        self.set_point(point)

        self.set_destination(dest)

        self.speed = speed

        self.heading = 0
        self.destination_heading = 0
        self.stamp = datetime.now()

        self.route = []
        self.length = 0

        self.router = router

    def point(self):
        """
        :return: LatLon point object with agent's current location
        """
        return LatLon(Latitude(self.lat),
                      Longitude(self.lon))

    def set_point(self, point):
        """
        Get lat and lon from LatLon point object, set them as agent's point.

        :param point: set agent's point to here

        :type point: LatLon point object
        """
        self.lat = float(point.lat)
        self.lon = float(point.lon)

    def destination(self):
        """
        :return: LatLon point object with agent's destination point
        """
        return LatLon(Latitude(self.dest_lat),
                      Longitude(self.dest_lon))

    def set_destination(self, point):
        """
        Get lat and lon from LatLon point object, set them as agent's
        destination point.

        :param point: set agent's destination to point

        :type point: LatLon point
        """
        self.dest_lat = float(point.lat)
        self.dest_lon = float(point.lon)

    def update(self, new_point, update_speed=False):
        """
        Updates time stamp and speed.

        uses @new_point to update:
         - point
         - heading
         - destination_heading
         - speed, if update_speed=True

        :param new_point: new current point to update to
        :param bool update_speed: wether to update agent's speed attribute
        :type new_point: LatLon point
        """
        
        self.heading = self.point().heading_initial(new_point)
        self.destination_heading = new_point.heading_initial(
            self.destination())

        if update_speed:
            tdelta = datetime.now() - self.stamp
            seconds = tdelta.total_seconds()
            distance = self.point().distance(new_point) / 1000.0
            self.speed = distance / seconds

        self.stamp = datetime.now()
        self.set_point(new_point)

    def heading_to(self, other_point):
        """
        :return: Heading from my point to @other_point, in degrees.
        :rtype: float

        :param other_point: return heading from agent's point to here
        :type other_point: LatLon point
        """
        return self.point().heading_initial(other_point)

    def distance_to(self, other_point):
        """
        :return: distance from agent to another point, in metres.
        :rtype: float

        :param other_point: return distance from agent's point to here
        :type other_point: LatLon point
        """
        return self.point().distance(other_point) * 1000.0

    def got_there(self):
        """
        :return: True if one step or less away
        :rtype: bool
        """
        if self.distance_to(self.destination()) < self.speed:
            return True
        else:
            return False

    def update_route(self, points=[]):
        """
        Query route server for points connecting current location to
        destination.

        If @points is given, route connects current location, sequence
        of points, and destination.

        :param points: list of LatLon points
        :return: True if succesful update of route, False if route is empty
        """
        assert self.router is not None
        
        route = self.router.get_route(points=[self.point(), ]
                                      + points
                                      + [self.destination(), ],
                                      speed=self.speed)
        if route:
            self.route = route
            self.length = self.router.length
            return True
        else:
            return False

    def step(self):
        """
        Calls update method to move agent to next point in route.
        Pops first item of route point list.
        """
        if self.route:
            p = self.route.pop(0)
            p = LatLon(Latitude(p[1]),
                       Longitude(p[0]))
        else:
            p = self.destination()

        self.update(p)

    def __str__(self):
        return "<A-%s %0.2fm @%sm/s %s>" % (id(self),
                                            self.distance_to(
                                                self.destination()),
                                            self.speed,
                                            self.point())
