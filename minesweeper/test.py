from minesweeper import Minesweeper, MinesweeperAI, Sentence


sentence = Sentence(["A", "B", "C"], 2)
print(sentence.known_mines())
print(sentence.known_safes())
print(sentence)
sentence.mark_mine("A")
sentence.mark_safe("B")
print(sentence.known_mines())
print(sentence.known_safes())
print(sentence)

ai = MinesweeperAI(height=8, width=8)
ai.mark_mine((1,2))
print(ai.knowledge)
ai.add_knowledge((1,3), 3)
print(ai.knowledge)
print(ai.mines)