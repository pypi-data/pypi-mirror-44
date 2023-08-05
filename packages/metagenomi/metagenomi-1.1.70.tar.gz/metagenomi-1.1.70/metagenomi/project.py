from boto3.dynamodb.conditions import Key, Attr


from metagenomi.db import dbconn
from metagenomi.models.assembly import Assembly
from metagenomi.models.sequencing import Sequencing
from metagenomi.models.sample import Sample
from metagenomi.base import MgObj
import time


class MgProject:
    '''
    A representation of a lot of MgObjects
    '''

    def __init__(self, mgproject, db=dbconn, check=False, derive_associations=False, load=False):
        self.db = db
        self.check = check

        self.mgproject = mgproject
        self.sequencings = []
        self.assemblies = []
        self.samples = []
        self.association_map = {}

        start = time.time()
        if self.mgproject == 'ALL':
            print('Loading all via scan')
            self.items = self.scan()
        else:
            self.items = self.query(self.mgproject)
        end = time.time()
        print(f'Queried {len(self.items)} in {end-start} seconds')

        if load:
            self.load_assemblies()
            self.load_sequencings()
            self.load_samples()

        if derive_associations:
            self.derive_associations()

    def load_assemblies(self):
        ###############
        start = time.time()
        assemblies = [i for i in self.items if i['mgtype'] == 'assembly']
        self.assemblies = [Assembly(db=self.db, check=self.check, **i) for i in assemblies]

        end = time.time()
        # print(f'Loaded {len(self.assemblies)} assemblies in {end-start} seconds')

    def load_sequencings(self):
        ###############
        start = time.time()
        sequencings = [i for i in self.items if i['mgtype'] == 'sequencing']
        self.sequencings = [Sequencing(db=self.db, check=self.check, **i) for i in sequencings]
        end = time.time()
        # print(f'Loaded {len(self.sequencings)} sequencings in {end-start} seconds')

    def load_samples(self):
        start = time.time()
        self.samples = [Sample(db=self.db, check=self.check, **i) for i in self.items
                        if i['mgtype'] == 'sample']
        end = time.time()
        # print(f'Loaded {len(self.samples)} samples in {end-start} seconds')

    def query(self, value, index='mgproject-mgtype-index', key='mgproject'):
        """
        Queries the database given a value, index, and key.
        First selects the index, and then returns all items (in a pageinated
        fasion where Key(key).eq(value).
        """
        print('Querying the database')

        response = self.db.table.query(
            IndexName=index,
            KeyConditionExpression=Key('mgproject').eq(value)
            )

        items = response['Items']
        while True:
            print(f'Loaded {len(items)} items')
            if response.get('LastEvaluatedKey'):
                response = self.db.table.query(
                    IndexName=index,
                    KeyConditionExpression=Key('mgproject').eq(value),
                    ExclusiveStartKey=response['LastEvaluatedKey']
                    )
                items += response['Items']
            else:
                break

        return items

    def scan(self, filter_key=None, filter_value=None, comparison='equals'):
        """
        not currently in use
        """

        if filter_key and filter_value:
            if comparison == 'equals':
                filtering_exp = Key(filter_key).eq(filter_value)
            elif comparison == 'contains':
                filtering_exp = Attr(filter_key).contains(filter_value)

            response = self.db.table.scan(
                FilterExpression=filtering_exp)

            items = response['Items']
            while True:
                print(f'Loaded {len(items)} items')
                if response.get('LastEvaluatedKey'):
                    response = self.db.table.scan(
                        ExclusiveStartKey=response['LastEvaluatedKey'],
                        FilterExpression=filtering_exp
                        )
                    items += response['Items']
                else:
                    break

            return items

        else:
            response = self.db.table.scan()

            items = response['Items']
            while True:
                print(f'Loaded {len(items)} items')
                if response.get('LastEvaluatedKey'):
                    response = self.db.table.scan(
                        ExclusiveStartKey=response['LastEvaluatedKey']
                        )
                    items += response['Items']
                else:
                    break

            return items

    def derive_associations(self):
        '''

        '''
        for mgobj in self.assemblies + self.samples + self.sequencings:
            for type, mgobj_list in mgobj.associated.items():
                for o in mgobj_list:
                    if not o == 'None':
                        connection = self.find_mgobj(o)
                        if mgobj in self.association_map:
                            self.association_map[
                                mgobj
                                ] = self.association_map[mgobj] + [connection]
                        else:
                            self.association_map[mgobj] = [connection]

    def find_mgobj(self, o):
        '''
        Given the mgid of an object, return the instance of that object.
        TODO: Test speed of this function
        '''
        if isinstance(o, MgObj):
            return o

        for i in self.assemblies + self.samples + self.sequencings:
            if i.mgid == o:
                return i

        raise ValueError(f'Object {o} is not in this project')
