import os

from stetl.etl import ETL
from stetl.filters.packetbuffer import PacketBuffer
from stetl.filters.regexfilter import RegexFilter
from tests.stetl_test_case import StetlTestCase

class RegexFilterTest(StetlTestCase):
    """Unit tests for RegexFilter"""

    def setUp(self):
        super(RegexFilterTest, self).setUp()

        # Initialize Stetl
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        cfg_dict = {'config_file': os.path.join(curr_dir, 'configs/regexfilter.cfg')}
        self.etl = ETL(cfg_dict)
    
    def test_class(self):
        chain = StetlTestCase.get_chain(self.etl)
        section = StetlTestCase.get_section(chain, 1)
        class_name = self.etl.configdict.get(section, 'class')
        
        self.assertEqual('stetl.filters.regexfilter.RegexFilter', class_name)
    
    def test_instance(self):
        chain = StetlTestCase.get_chain(self.etl)

        self.assertTrue(isinstance(chain.get_by_index(1), RegexFilter))
        
    def test_execute(self):
        chain = StetlTestCase.get_chain(self.etl)
        chain.run()

        buffer_filter = chain.get_by_class(PacketBuffer)
        packet_list = buffer_filter.packet_list

        self.assertEqual(packet_list[0].data.get('elemtype'), "BuildingInstallation")
        self.assertEqual(int(packet_list[0].data.get('featurecount')), 1162)
