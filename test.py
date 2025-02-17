import unittest
from unittest.mock import patch
from flow_log_parser import *



class test_flow_log(unittest.TestCase):
    def read_file(self, filename):
        file = open(filename)
        content = file.read()
        file.close()
        return content
    
    @patch('flow_log_parser.FLOW_LOG_FILENAME', 'tests/test1.txt')
    @patch('flow_log_parser.TAG_COUNT_FILENAME', 'tests/test1_out1.txt')
    @patch('flow_log_parser.PORT_PROTOCOL_FILENAME', 'tests/test1_out2.txt')
    @patch('flow_log_parser.FLOW_LOGS', {})
    @patch('flow_log_parser.PORT_PROTOCOL_COUNT', {})
    @patch('flow_log_parser.UNTAGGED_FLOW_LOGS', 0)
    def test_basic(self):
        main()
        content = self.read_file('tests/test1_out1.txt')
        self.assertEqual(content, 'Tag,Count\nsv_P1,1\n')
        content = self.read_file('tests/test1_out2.txt')
        self.assertEqual(content, 'Port,Protocol,Count\n25,tcp,1\n')

    @patch('flow_log_parser.FLOW_LOG_FILENAME', 'tests/test2.txt')
    @patch('flow_log_parser.TAG_COUNT_FILENAME', 'tests/test2_out1.txt')
    @patch('flow_log_parser.PORT_PROTOCOL_FILENAME', 'tests/test2_out2.txt')
    @patch('flow_log_parser.FLOW_LOGS', {})
    @patch('flow_log_parser.PORT_PROTOCOL_COUNT', {})
    @patch('flow_log_parser.UNTAGGED_FLOW_LOGS', 0)
    def test_untagged(self):
        main()
        content = self.read_file('tests/test2_out1.txt')
        self.assertEqual(content, 'Tag,Count\nsv_P1,1\nUntagged,1\n')
        content = self.read_file('tests/test2_out2.txt')
        self.assertEqual(content, 'Port,Protocol,Count\n25,tcp,1\n200,tcp,1\n')
    
    @patch('flow_log_parser.FLOW_LOG_FILENAME', 'tests/test3.txt')
    @patch('flow_log_parser.TAG_COUNT_FILENAME', 'tests/test3_out1.txt')
    @patch('flow_log_parser.PORT_PROTOCOL_FILENAME', 'tests/test3_out2.txt')
    @patch('flow_log_parser.FLOW_LOGS', {})
    @patch('flow_log_parser.PORT_PROTOCOL_COUNT', {})
    @patch('flow_log_parser.UNTAGGED_FLOW_LOGS', 0)
    def test_multiple_tags(self):
        main()
        content = self.read_file('tests/test3_out1.txt')
        self.assertEqual(content, 'Tag,Count\nsv_P1,1\nUntagged,1\n')
        content = self.read_file('tests/test3_out2.txt')
        self.assertEqual(content, 'Port,Protocol,Count\n25,tcp,1\n200,tcp,1\n')
    
    @patch('flow_log_parser.FLOW_LOG_FILENAME', 'tests/test4.txt')
    @patch('flow_log_parser.TAG_COUNT_FILENAME', 'tests/test4_out1.txt')
    @patch('flow_log_parser.PORT_PROTOCOL_FILENAME', 'tests/test4_out2.txt')
    @patch('flow_log_parser.FLOW_LOGS', {})
    @patch('flow_log_parser.PORT_PROTOCOL_COUNT', {})
    @patch('flow_log_parser.UNTAGGED_FLOW_LOGS', 0)
    def test_multiple_same_tags(self):
        main()
        content = self.read_file('tests/test4_out1.txt')
        self.assertEqual(content, 'Tag,Count\nsv_P1,2\nsv_P4,2\nUntagged,2\n')
        content = self.read_file('tests/test4_out2.txt')
        self.assertEqual(content, 'Port,Protocol,Count\n25,tcp,2\n22,tcp,2\n100,tcp,2\n')
    

if __name__ == '__main__':
    unittest.main()
