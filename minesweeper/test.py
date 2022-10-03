import unittest
from minesweeper import Minesweeper, MinesweeperAI, Sentence


class Tests(unittest.TestCase):

    def test_known_mines_false(self):
        """ Check known_mines when it is inconclusive"""
        sentence = Sentence(["A", "B", "C"], 2)
        self.assertFalse(sentence.known_mines())
    
    def test_known_mines_true(self):
        """ Check known_mines when it is conclusive"""
        sentence = Sentence(["A", "B", "C"], 3)
        self.assertEqual({"A", "B", "C"}, sentence.known_mines())
    
    def test_known_safes(self):
        """ Check known_safes"""
        sentence = Sentence(["A", "B", "C"], 0)
        self.assertEqual({"A", "B", "C"}, sentence.known_safes())
    
    def test_mark_mine(self):
        """ Check mark_mine"""
        sentence = Sentence(["A", "B", "C"], 2)
        sentence.mark_mine("A")
        self.assertEqual(Sentence(["B", "C"], 1), sentence)

    def test_mark_safe(self):
        """ Check mark_safe"""
        sentence = Sentence(["A", "B", "C"], 2)
        sentence.mark_safe("A")
        self.assertEqual(Sentence(["B", "C"], 2), sentence)

    
    def test_add_knowledge(self):
        """ Check add_knowledge"""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((0,0), 1)
        ai.add_knowledge((0,1), 1)
        ai.add_knowledge((0,2), 1)
        ai.add_knowledge((2,1), 2)
        self.assertEqual(ai.mines, {(1,1)})
    
    def test_make_safe_move(self):
        """ Check make_safe_move """
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((0,0), 1)
        ai.add_knowledge((0,1), 1)
        ai.add_knowledge((0,2), 1)
        ai.add_knowledge((2,1), 2)
        self.assertIn(ai.make_safe_move(), {(1,0),(1,2)})
    


if __name__ == "__main__":
    a ={1,2, 3}
    b =[2,3,5,4]
    print(a-b)
    #c= set([(i,j) for i in range(8) for j in range(8)])
    print(c)
    unittest.main()