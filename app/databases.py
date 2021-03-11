class BinaryTrajectories:
    def __init__(self, suffix):
        self.suffix = suffix

    fields = ['kstar',
              'mass0',
              'mass',
              'lumin',
              'rad',
              'teff',
              'massc',
              'radc',
              'menv',
              'renv',
              'epoch',
              'ospin',
              'deltam'
              'rrol', ]

    @property
    def attributes(self):
        return self.fields

    @property
    def field_map(self):
        """Returns mapping for {field_name:display_name}"""
        return {
            field + self.suffix:field for field in BinaryTrajectories.fields
        }

DATABASE_MAP = {
    'binary-trajectories-1': BinaryTrajectories('_1'),
    'binary-trajectories-2': BinaryTrajectories('_2')
}

def get_databases():
    """List the databases"""
    return list(DATABASE_MAP.keys())

def get_database(database):
    """Return the database instance"""
    return DATABASE_MAP.get(database)

def get_database_attributes(database):
    """Return the attributes of the given database"""
    return get_database(database).attributes
