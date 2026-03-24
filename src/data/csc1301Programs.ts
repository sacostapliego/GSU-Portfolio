import blackjackOriginalCode from '../../1301 - Principles of Computer Science I/original-code/BlackJack.py?raw'
import bravesOriginalCode from '../../1301 - Principles of Computer Science I/original-code/Braves.py?raw'
import dairyQueenOriginalCode from '../../1301 - Principles of Computer Science I/original-code/Dairy Queen.py?raw'
import homeOriginalCode from '../../1301 - Principles of Computer Science I/original-code/Home.py?raw'
import homework1OriginalCode from '../../1301 - Principles of Computer Science I/original-code/Homework 1.py?raw'
import lab8OriginalCode from '../../1301 - Principles of Computer Science I/original-code/Lab 8.py?raw'
import luckySevensOriginalCode from '../../1301 - Principles of Computer Science I/original-code/Lucky Sevens.py?raw'
import newtonOriginalCode from '../../1301 - Principles of Computer Science I/original-code/Newton.py?raw'
import newtonRecurseOriginalCode from '../../1301 - Principles of Computer Science I/original-code/newton_recurse.py?raw'
import panamanianFlagOriginalCode from '../../1301 - Principles of Computer Science I/original-code/Panamanian Flag.py?raw'
import phoneNumberOriginalCode from '../../1301 - Principles of Computer Science I/original-code/Phone Number.py?raw'
import swappingVariablesOriginalCode from '../../1301 - Principles of Computer Science I/original-code/Swapping Variables.py?raw'
import ticTacToeOriginalCode from '../../1301 - Principles of Computer Science I/original-code/TicTacToe.py?raw'

import blackjackPyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/BlackJack.py?raw'
import bravesPyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/Braves.py?raw'
import dairyQueenPyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/Dairy Queen.py?raw'
import homePyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/Home.py?raw'
import homework1PyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/Homework 1.py?raw'
import lab8PyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/Lab 8.py?raw'
import luckySevensPyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/Lucky Sevens.py?raw'
import newtonPyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/Newton.py?raw'
import newtonRecursePyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/newton_recurse.py?raw'
import panamanianFlagPyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/Panamanian Flag.py?raw'
import phoneNumberPyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/Phone Number.py?raw'
import swappingVariablesPyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/Swapping Variables.py?raw'
import ticTacToePyodideCode from '../../1301 - Principles of Computer Science I/pyodide-adapted/TicTacToe.py?raw'

export interface Csc1301Program {
  id: string
  title: string
  fileName: string
  description: string
  runCommand: string
  originalSourceCode: string
  pyodideSourceCode: string
  suggestedInput?: string
}

export const csc1301Programs: Csc1301Program[] = [
  {
    id: 'blackjack',
    title: 'Blackjack',
    fileName: 'BlackJack.py',
    description: 'Card game simulation and flow control practice.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/BlackJack.py"',
    originalSourceCode: blackjackOriginalCode,
    pyodideSourceCode: blackjackPyodideCode,
    suggestedInput: '20\n2\ny\n2\nn\n',
  },
  {
    id: 'braves',
    title: 'Braves',
    fileName: 'Braves.py',
    description: 'Conditional logic and formatted output exercise.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Braves.py"',
    originalSourceCode: bravesOriginalCode,
    pyodideSourceCode: bravesPyodideCode,
    suggestedInput: '1\nacuna\n',
  },
  {
    id: 'dairy-queen',
    title: 'Dairy Queen',
    fileName: 'Dairy Queen.py',
    description: 'Input handling and branch logic assignment.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Dairy Queen.py"',
    originalSourceCode: dairyQueenOriginalCode,
    pyodideSourceCode: dairyQueenPyodideCode,
    suggestedInput: 'y\nn\nn\ny\ny\nn\n',
  },
  {
    id: 'home',
    title: 'Home',
    fileName: 'Home.py',
    description: 'Basic Python syntax and variables lab.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Home.py"',
    originalSourceCode: homeOriginalCode,
    pyodideSourceCode: homePyodideCode,
  },
  {
    id: 'homework-1',
    title: 'Homework 1',
    fileName: 'Homework 1.py',
    description: 'Foundational program structure and calculations.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Homework 1.py"',
    originalSourceCode: homework1OriginalCode,
    pyodideSourceCode: homework1PyodideCode,
    suggestedInput: '300\n12\n',
  },
  {
    id: 'lab-8',
    title: 'Lab 8',
    fileName: 'Lab 8.py',
    description: 'Looping and control-flow focused lab work.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Lab 8.py"',
    originalSourceCode: lab8OriginalCode,
    pyodideSourceCode: lab8PyodideCode,
    suggestedInput: '5\n10\n3\n7\n',
  },
  {
    id: 'lucky-sevens',
    title: 'Lucky Sevens',
    fileName: 'Lucky Sevens.py',
    description: 'Random simulation and iterative logic practice.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Lucky Sevens.py"',
    originalSourceCode: luckySevensOriginalCode,
    pyodideSourceCode: luckySevensPyodideCode,
    suggestedInput: '25\n',
  },
  {
    id: 'newton',
    title: 'Newton',
    fileName: 'Newton.py',
    description: 'Numerical method implementation using iteration.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Newton.py"',
    originalSourceCode: newtonOriginalCode,
    pyodideSourceCode: newtonPyodideCode,
    suggestedInput: '49\n\n',
  },
  {
    id: 'newton-recurse',
    title: 'Newton Recurse',
    fileName: 'newton_recurse.py',
    description: 'Newton method variant using recursion.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/newton_recurse.py"',
    originalSourceCode: newtonRecurseOriginalCode,
    pyodideSourceCode: newtonRecursePyodideCode,
    suggestedInput: '64\n\n',
  },
  {
    id: 'panamanian-flag',
    title: 'Panamanian Flag',
    fileName: 'Panamanian Flag.py',
    description: 'Graphical drawing exercise using Python libraries.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Panamanian Flag.py"',
    originalSourceCode: panamanianFlagOriginalCode,
    pyodideSourceCode: panamanianFlagPyodideCode,
  },
  {
    id: 'phone-number',
    title: 'Phone Number',
    fileName: 'Phone Number.py',
    description: 'String parsing and formatting assignment.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Phone Number.py"',
    originalSourceCode: phoneNumberOriginalCode,
    pyodideSourceCode: phoneNumberPyodideCode,
  },
  {
    id: 'swapping-variables',
    title: 'Swapping Variables',
    fileName: 'Swapping Variables.py',
    description: 'Variable manipulation and assignment basics.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/Swapping Variables.py"',
    originalSourceCode: swappingVariablesOriginalCode,
    pyodideSourceCode: swappingVariablesPyodideCode,
    suggestedInput: '1\n2\n3\n4\n',
  },
  {
    id: 'tic-tac-toe',
    title: 'Tic Tac Toe',
    fileName: 'TicTacToe.py',
    description: 'Checks horizontal, vertical, and diagonal wins from user input.',
    runCommand: 'python "1301 - Principles of Computer Science I/original-code/TicTacToe.py"',
    originalSourceCode: ticTacToeOriginalCode,
    pyodideSourceCode: ticTacToePyodideCode,
    suggestedInput: 'XOX\nOOX\nXXO\n',
  },
]
