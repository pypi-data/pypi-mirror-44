from metagenomi.models.modelbase import MgModel
from metagenomi.tasks.assemblystats import AssemblyStats
from metagenomi.tasks.prodigal import Prodigal
from metagenomi.tasks.mapping import Mapping
from metagenomi.tasks.minced import Minced
from metagenomi.tasks.crisprconnection import CrisprConnection
from metagenomi.tasks.jgimetadata import JgiMetadata

# from metagenomi.logger import logger


class Assembly(MgModel):
    # Possible tasks:
    # Mapping, Megahit, TODO:Prodigal
    def __init__(self, mgid, **data):
        MgModel.__init__(self, mgid, **data)

        self.s3path = self.d.get('s3path')

        self.mgtype = 'assembly'
        if 'mgtype' in self.d:
            self.mgtype = self.d['mgtype']

        self.mappings = None
        if 'Mappings' in self.d:
            self.mappings = []
            for m in self.d['Mappings']:
                self.mappings.append(Mapping(self.mgid, db=self.db, check=self.check, **m))

        self.assembly_stats = None
        if 'AssemblyStats' in self.d:
            self.assembly_stats = AssemblyStats(self.mgid,
                                                db=self.db, check=self.check, **self.d['AssemblyStats'])

        self.prodigal = None
        if 'Prodigal' in self.d:
            self.prodigal = Prodigal(self.mgid, db=self.db, check=self.check, **self.d['Prodigal'])

        self.jgi_metadata = None
        if 'JgiMetadata' in self.d:
            self.jgi_metadata = JgiMetadata(self.mgid, db=self.db, check=self.check,  **self.d['JgiMetadata'])

        self.minced = None
        if 'Minced' in self.d:
            self.minced = Minced(self.mgid, db=self.db, check=self.check, **self.d['Minced'])

        self.crispr_connections = None
        if 'CrisprConnections' in self.d:
            self.crispr_connections = []
            for m in self.d['CrisprConnections']:
                self.crispr_connections.append(CrisprConnection(self.mgid, db=self.db, check=self.check, **m))


        # No MgTasks are required. TODO: Except perhaps mapping?
        self.schema = {**self.schema, **{
            'Prodigal': {'type': 'dict'},
            'AssemblyStats': {'type': 'dict'},
            'Mappings': {'type': 'list'},
            'JgiMetadata': {'type': 'dict'},
            'Minced': {'type': 'dict'},
            'CrisprConnection': {'type': 'list'},
            'mgtype': {'type': 'string',
                       'allowed': ['assembly'],
                       'required': True}
            },
            's3path': {'type': 's3file', 'required': True},
            'associated': {'type': 'dict',
                           'required': True,
                           'schema': {'sequencing': {
                                'type': 'list',
                                'schema': {'type': ['mgid',
                                                    'nonestring']},
                                'required': True
                                },
                            }
                        }
            }

        if self.check:
            self.validate()

    def update_s3path(self, newpath, write=True):
        self.s3path = newpath

        if write:
            if self.validate():
                self.update('s3path', newpath)

    def get_filtered_contigs(self):
        if self.prodigal:
            ctgs = self.prodigal.pullseq_contigs
            return ctgs
        else:
            e = f'No filtered contigs, prodigal has not been run'
            raise ValueError(e)

    def generate_prodigal_cmd(self, cutoff=1000):
        genes = f"{self.s3path}.genes"
        faa = f"{self.s3path}.genes.faa"
        minx = self.s3path.split('.')[0]+f'_min{cutoff}.fa'

        cmd = f'python submit_prodigal_job.py --input {self.s3path} '
        cmd += f'--output {minx} --outgenes {genes} --outfaa {faa}'

        return(cmd)

    def generate_minced_cmd(self, filtered_ctgs=True, overrides=None):
        '''
        '''
        # if filtered_ctgs:
        #     ctgs = self.get_filtered_contigs()
        # else:
        #     ctgs = self.s3path

        cmd = f'python submit_minced.py --mgid {self.mgid} --gff'
        return(cmd)

        # out = ctgs.rsplit('.', 1)[0] + '.' + 'minced'
        # cmd = f'python submit_minced.py --infile {ctgs} --out {out} '
        # if overrides is not None:
        #     cmd += overrides
        #
        # return(cmd)
