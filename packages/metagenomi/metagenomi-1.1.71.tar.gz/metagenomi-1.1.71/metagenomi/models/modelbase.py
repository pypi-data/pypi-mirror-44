from abc import ABCMeta

from boto3.dynamodb.conditions import Key

from metagenomi.base import MgObj
from metagenomi.logger import logger
from metagenomi.helpers import get_time

# from metagenomi.models.assembly import Assembly
# from metagenomi.models.sequencing import Sequencing
# from metagenomi.models.sample import Sample


class MgModel(MgObj):
    '''
    MgModel - base class for all models
    '''
    __metaclass__ = ABCMeta

    def __init__(self, mgid, **data):
        MgObj.__init__(self, mgid, **data)

        # If data not passed, object is loaded in the MgObj base class
        self.associated = self.d.get('associated', {})

        if 'created' in self.d:
            self.created = self.d['created']
        else:
            self.created = get_time()

        if 'mgproject' in self.d:
            self.mgproject = self.d['mgproject'].upper()
        else:
            self.mgproject = self.mgid[:4].upper()

        self.schema = {
            **self.schema, **{
                'mgtype': {'type': 'string', 'required': True,
                           'allowed': ['sequencing', 'assembly', 'sample']},
                'associated': {'type': 'dict', 'required': True, 'schema': {
                    'sequencing': {'type': 'list', 'schema': {'type': 'mgid'}},
                    'assembly':  {'type': 'list', 'schema': {'type': 'mgid'}},
                    'sample':  {'type': 'list', 'schema': {'type': 'mgid'}},
                    }
                },
                'created': {'type': 'datestring', 'required': True},
                'mgproject': {'type': 'string', 'required': True,
                              'maxlength': 4, 'minlength': 4}
            }
        }

    # def add_association(self, mgtype, mgid, end=False, write=True):
    #     '''
    #     Adds association to both self and the affected object
    #     '''
    #     if mgtype in self.associated:
    #         if self.associated[mgtype] == ['None']:
    #             self.associated[mgtype] = [mgid]
    #         else:
    #             if mgid not in self.associated[mgtype]:
    #                 self.associated[mgtype] = self.associated[mgtype] + [mgid]
    #     else:
    #         self.associated[mgtype] = [mgid]
    #
    #     if write:
    #         self.write(force=True)
    #
    #     if end:
    #         return
    #     else:
    #         if mgtype == 'sequencing':
    #             assoc = Sequencing(mgid, db=self.db)
    #         elif mgtype == 'sample':
    #             assoc = Sample(mgid, db=self.db)
    #         else:
    #             assoc = Assembly(mgid, db=self.db)
    #
    #         assoc.add_association(self.whoami().lower(), self.mgid, end=True)

    def write(self, force=False, ignore_exceptions=True, dryrun=False):
        '''
        Write this object to the database - over-ridden in other derived
        classes when needed
        '''

        d = self.to_dict(validate=True, clean=True)

        # Add it back in at the appropriate spot
        d['mgid'] = self.mgid

        response = self.db.table.query(
            KeyConditionExpression=Key('mgid').eq(self.mgid))

        if dryrun:
            print('--- dry run ----')
            print(f'Would write to {self.db.table}')
            print(d)
            return

        if len(response['Items']) < 1:
            # new document
            response = self.db.table.put_item(
                Item=d
            )
            # TODO: validate we got a good response from db
            logger.info(f'Wrote {response} to db')

        else:
            if force:
                response = self.db.table.put_item(
                    Item=d
                )
                # TODO: validate we got a good response from db
                logger.info(f'Wrote {response} to db')
            else:
                msg = f'{self.mgid} is already in DB - cannot re-write'
                logger.debug(msg)
                if ignore_exceptions:
                    print(f'WARNING: {msg}')
                else:
                    raise ValueError(msg)

    def update(self, key, value, dryrun=False):
        '''
        TODO: VALIDATION???

        '''

        if dryrun:
            print('Dry run')
            print(f'Would update {key} to {value}')

        else:
            response = self.db.table.update_item(
                                Key={
                                    'mgid': self.mgid
                                },
                                UpdateExpression=f"set {key} = :r",
                                ExpressionAttributeValues={
                                    ':r': value
                                },
                                ReturnValues="UPDATED_NEW"
                            )
            return response
