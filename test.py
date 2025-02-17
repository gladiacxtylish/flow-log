import unittest
from unittest.mock import patch
from flow_log_parser import *


class test_flow_log(unittest.TestCase):
    def read_file(self, filename):
        """
        Helper method to read the file content
        """
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
        """
        This tests the most basic things
        """
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
        """
        This tests the untagged log
        """
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
        """
        Extensive tests on different kind of tags
        """
        main()
        content = self.read_file('tests/test3_out1.txt')
        self.assertEqual(content, 'Tag,Count\nsv_P1,2\nsv_P4,2\nUntagged,2\n')
        content = self.read_file('tests/test3_out2.txt')
        self.assertEqual(content, 'Port,Protocol,Count\n25,tcp,2\n22,tcp,2\n100,tcp,2\n')
    
    @patch('flow_log_parser.FLOW_LOG_FILENAME', 'tests/test4.txt')
    @patch('flow_log_parser.TAG_COUNT_FILENAME', 'tests/test4_out1.txt')
    @patch('flow_log_parser.PORT_PROTOCOL_FILENAME', 'tests/test4_out2.txt')
    @patch('flow_log_parser.FLOW_LOGS', {})
    @patch('flow_log_parser.PORT_PROTOCOL_COUNT', {})
    @patch('flow_log_parser.UNTAGGED_FLOW_LOGS', 0)
    def test_multiple_same_tags(self):
        """
        This tests different kind of protocols
        """
        main()
        content = self.read_file('tests/test4_out1.txt')
        self.assertEqual(content, 'Tag,Count\nsv_P1,1\nsv_P4,1\nUntagged,4\n')
        content = self.read_file('tests/test4_out2.txt')
        self.assertEqual(content, 'Port,Protocol,Count\n25,tcp,1\n25,st,1\n22,tcp,1\n22,st,1\n100,tcp,1\n100,st,1\n')
    

if __name__ == '__main__':
    unittest.main()
