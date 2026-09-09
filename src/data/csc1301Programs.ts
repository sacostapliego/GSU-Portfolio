import blackjackCode from '../../1301 - Principles of Computer Science I/original-code/BlackJack.py?raw'
import bravesCode from '../../1301 - Principles of Computer Science I/original-code/Braves.py?raw'
import dairyQueenCode from '../../1301 - Principles of Computer Science I/original-code/Dairy Queen.py?raw'
import homeCode from '../../1301 - Principles of Computer Science I/original-code/Home.py?raw'
import homework1Code from '../../1301 - Principles of Computer Science I/original-code/Homework 1.py?raw'
import lab8Code from '../../1301 - Principles of Computer Science I/original-code/Lab 8.py?raw'
import luckySevensCode from '../../1301 - Principles of Computer Science I/original-code/Lucky Sevens.py?raw'
import newtonCode from '../../1301 - Principles of Computer Science I/original-code/Newton.py?raw'
import newtonRecurseCode from '../../1301 - Principles of Computer Science I/original-code/newton_recurse.py?raw'
import panamanianFlagCode from '../../1301 - Principles of Computer Science I/original-code/Panamanian Flag.py?raw'
import phoneNumberCode from '../../1301 - Principles of Computer Science I/original-code/Phone Number.py?raw'
import swappingVariablesCode from '../../1301 - Principles of Computer Science I/original-code/Swapping Variables.py?raw'
import ticTacToeCode from '../../1301 - Principles of Computer Science I/original-code/TicTacToe.py?raw'

export interface Csc1301Program {
  id: string
  title: string
  fileName: string
  description: string
  runCommand: string
  sourceCode: string
  suggestedInput?: string
}

export const csc1301Programs: Csc1301Program[] = [
  {
    id: 'blackjack',
    title: 'Blackjack',
    fileName: 'BlackJack.py',
    description: 'Card game simulation and flow control practice.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/BlackJack.py"',
    sourceCode: blackjackCode,
    suggestedInput: '20\n2\ny\n2\nn\n',
  },
  {
    id: 'braves',
    title: 'Braves',
    fileName: 'Braves.py',
    description: 'Conditional logic and formatted output exercise.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Braves.py"',
    sourceCode: bravesCode,
    suggestedInput: '1\nacuna\n',
  },
  {
    id: 'dairy-queen',
    title: 'Dairy Queen',
    fileName: 'Dairy Queen.py',
    description: 'Input handling and branch logic assignment.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Dairy Queen.py"',
    sourceCode: dairyQueenCode,
    suggestedInput: 'y\nn\nn\ny\ny\nn\n',
  },
  {
    id: 'home',
    title: 'Home',
    fileName: 'Home.py',
    description: 'Basic Python syntax and variables lab.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Home.py"',
    sourceCode: homeCode,
  },
  {
    id: 'homework-1',
    title: 'Homework 1',
    fileName: 'Homework 1.py',
    description: 'Foundational program structure and calculations.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Homework 1.py"',
    sourceCode: homework1Code,
    suggestedInput: '300\n12\n',
  },
  {
    id: 'lab-8',
    title: 'Lab 8',
    fileName: 'Lab 8.py',
    description: 'Looping and control-flow focused lab work.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Lab 8.py"',
    sourceCode: lab8Code,
    suggestedInput: '5\n10\n3\n7\n',
  },
  {
    id: 'lucky-sevens',
    title: 'Lucky Sevens',
    fileName: 'Lucky Sevens.py',
    description: 'Random simulation and iterative logic practice.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Lucky Sevens.py"',
    sourceCode: luckySevensCode,
    suggestedInput: '25\n',
  },
  {
    id: 'newton',
    title: 'Newton',
    fileName: 'Newton.py',
    description: 'Numerical method implementation using iteration.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Newton.py"',
    sourceCode: newtonCode,
    suggestedInput: '49\n\n',
  },
  {
    id: 'newton-recurse',
    title: 'Newton Recurse',
    fileName: 'newton_recurse.py',
    description: 'Newton method variant using recursion.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/newton_recurse.py"',
    sourceCode: newtonRecurseCode,
    suggestedInput: '64\n\n',
  },
  {
    id: 'panamanian-flag',
    title: 'Panamanian Flag',
    fileName: 'Panamanian Flag.py',
    description: 'Graphical drawing exercise using Python libraries.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Panamanian Flag.py"',
    sourceCode: panamanianFlagCode,
  },
  {
    id: 'phone-number',
    title: 'Phone Number',
    fileName: 'Phone Number.py',
    description: 'String parsing and formatting assignment.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Phone Number.py"',
    sourceCode: phoneNumberCode,
  },
  {
    id: 'swapping-variables',
    title: 'Swapping Variables',
    fileName: 'Swapping Variables.py',
    description: 'Variable manipulation and assignment basics.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Swapping Variables.py"',
    sourceCode: swappingVariablesCode,
    suggestedInput: '1\n2\n3\n4\n',
  },
  {
    id: 'tic-tac-toe',
    title: 'Tic Tac Toe',
    fileName: 'TicTacToe.py',
    description: 'Checks horizontal, vertical, and diagonal wins from user input.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/TicTacToe.py"',
    sourceCode: ticTacToeCode,
    suggestedInput: 'XOX\nOOX\nXXO\n',
  },
]
