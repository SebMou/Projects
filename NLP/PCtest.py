import pandas as pd
import unittest
import PCAutocomplete

"""
Importing from PCAutocomplete, we create a trie and populate it with the entries
in our csv file, read in line 12. Directory should be changed accordingly.
"""

trie = PCAutocomplete.Trie()

possibs = pd.read_csv(r"C:\Users\Asus\Downloads\python-challenge-master\python-challenge-master\test_files\190titles.csv")

for row in possibs.itertuples():
    trie.insert(row.Name)
     
class Tests(unittest.TestCase):
 
    """
    Each test is conducted in the hopes that the expectation will be confirmed.
    Conducted tests are:
        - Does the list of results contain any
        - Is the list of results empty
        - Can we input special characters and receive a result, even if it is
            empty
        - Does a specific result appear
        - Does a false result no appear
        - Entry will appear if entire entry is searched
        
    """
    
    def setUp(self):
        pass
 
    def test_has(self):
        self.assertTrue(list(trie.complete("What")))
 
    def test_does_not_have(self):
        self.assertFalse(list(trie.complete("qwerty")))
    
    def test_special_character(self):
        self.assertIsNotNone(list(trie.complete("~")))

    def test_has_specific(self):
        self.assertTrue("WhatsApp Messenger" in list(trie.complete("What")))
 
    def test_not_specific(self):
        self.assertFalse("WhatsApp Messener" in list(trie.complete("What")))
        
    def test_has_complete_entry(self):
        self.assertTrue("WhatsApp Messenger" in list(trie.complete("WhatsApp Messenger")))
    
    
 
if __name__ == '__main__':
    unittest.main()