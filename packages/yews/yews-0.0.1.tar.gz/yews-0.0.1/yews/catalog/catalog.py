import warnings
import pandas as pd
from obspy import core

class Catalog(object):

    def __init__(self):
        """Initiate catalog object with events, stations, and arrivals."""

        self.events = None
        self.stations = None
        self.arrivals = None

        self._create_event_table()
        self._create_station_table()
        self._create_arrival_table()

    def __len__(self):
        """Number of events in the catalog."""

        return len(self.events.index)

    def _create_event_table(self):
        """Generate pandas tabel from loaded event info.

        """

        table = pd.DataFrame(self.load_events())
        self.events = table.drop_duplicates().reset_index(drop=True)

    def _create_station_table(self):
        """Generate pandas table from loaded station info.

        """

        table = pd.DataFrame(self.load_stations())
        self.stations = table.drop_duplicates().reset_index(drop=True)

    def _create_arrival_table(self):
        """Generate pandas table from loaded arrival info."""
        table = pd.DataFrame(self.load_arrivals())
        self.arrivals = table.drop_duplicates().reset_index(drop=True)

    def _check_event_table(self):
        """Check if event table has the columns for obspy event."""

        flag = True
        if ('time' not in self.events.columns):
            warnings.warn('Event table missing origin time.')
            flag = False

        if ('event_id' not in self.events.columns):
            warnings.warn('Event table missing event id.')
            flag = False

        if ('latitude' not in self.events.columns):
            warnings.warn('Event table missing latitude.')
            flag = False

        if ('longitude' not in self.events.columns):
            warnings.warn('Event table missing longitude.')
            flag = False

        if ('depth' not in self.events.columns):
            warnings.warn('Event table missing depth.')
            flag = False

        if ('magnitude' not in self.events.columns):
            warnings.warn('Event table missing magnitude.')
            flag = False

        return flag

    def _check_station_table(self):
        """Check if station table has the columns for obspy station."""

        flag = True
        if ('station_id' not in self.stations.columns):
            warnings.warn('Station table missing station id.')
            flag = False

        if ('latitude' not in self.stations.columns):
            warnings.warn('Station table missing latitude.')
            flag = False

        if ('longitude' not in self.stations.columns):
            warnings.warn('Station table missing longitude.')
            flag = False

        return flag

    def _check_arrival_table(self):
        """Check if arrival table has the columns for obspy pick."""

        flag = True
        if ('time' not in self.arrivals.columns):
            warnings.warn('Arrival table missing origin time.')
            flag = False

        if ('event_id' not in self.arrivals.columns):
            warnings.warn('Arrival table missing event id.')
            flag = False

        if ('station_id' not in self.arrivals.columns):
            warnings.warn('Arrival table missing station id.')
            flag = False

        if ('phase' not in self.arrivals.columns):
            warnings.warn('Arrival table missing phase.')
            flag = False

        return flag

    def network(self, name=''):
        """Produce obspy inventory based on station table."""

        if self._check_station_table():
            stations_list = []
            for idx, row in self.stations.iterrows():
                if 'elevation' in row.keys():
                    elevation = row['elevation']
                else:
                    elevation = 0

                stations_list.append(
                    core.inventory.Station(
                        row['station_id'],
                        row['latitude'],
                        row['longitude'],
                        elevation,
                    )
                )
        else:
            raise ValueError("Station table is incomplete.")

        net = core.inventory.Network(
            name,
            stations=stations_list,
        )

        return net

    def catalog(self):
        """Produce obspy catalog based on event and arrival tables."""

        if not self._check_arrival_table():
            raise ValueError("Arrival table is incomplete.")

        if not self._check_event_table():
            raise ValueError("Event table is incomplete.")

        event_list = []
        for  idx, row in self.events.iterrows():
            event_ri = core.event.ResourceIdentifier(
                id=f"smi:yews/event/{row['event_id']}"
            )

            origin_ri = core.event.ResourceIdentifier(
                id=f"smi:yews/origin/{row['event_id']}"
            )

            magnitude_ri = core.event.ResourceIdentifier(
                id=f"smi:yews/magnitude/{row['event_id']}"
            )

            picks = self.arrivals[self.arrivals['event_id']==row['event_id']]
            pick_list = []



    def load_events(self):
        """Custom function that returns info to populate event table.

        Note: 'event_id' must be one of the table columns.

        """

        raise NotImplemented

    def load_stations(self):
        """Custom function that returns info to populate station table.

        Note: 'station_id' must be one of the table columns.

        """

        raise NotImplemented

    def load_arrivals(self):
        """Custom function that returns info to populate arrival table.

        Note: 'event_id' and 'station_id' must be among the table columns.

        """

        raise NotImplemented

