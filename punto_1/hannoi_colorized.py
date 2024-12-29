# kind of hannoi with colorized rule (same color can't be on top of each other)

"""
A class that implements the Tower of Hanoi puzzle with an additional color rule.
The traditional size rule still applies (larger disks cannot be placed on smaller ones),
but disks of the same color cannot be placed on top of each other.
Each disk is represented as a tuple (size, color) where size is an integer and color is a string.
"""

class ColorHanoi:
    
    """
    Initialize the ColorHanoi puzzle with a set of disks.
    
    Args:
        disks (list): List of tuples where each tuple contains (size, color).
                      The disks should be ordered from largest to smallest.
    """
    
    def __init__(self, disks):
        self.moves = []
        self.disks = disks
        self.towers = {
            'A': list(disks),
            'B': [],
            'C': []
        }
        
    """
    Check if a move from source to target is valid.

    Args:
        source (str): The source tower ('A', 'B', or 'C').
        target (str): The target tower ('A', 'B', or 'C').

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    def is_valid_move(self, source, target):
        # No disk to move to same tower
        if not self.towers[source]:
            return False
        
        # obtain the disk to move and the disk on top of the target tower    
        moving_disk = self.towers[source][-1]
        
        # If target tower is empty, move is valid
        if not self.towers[target]:
            return True
         
        # obtain the disk on top of the target tower    
        target_disk = self.towers[target][-1]
        
        # Check size rule
        if moving_disk[0] > target_disk[0]:
            return False
            
        # Check color rule
        if moving_disk[1] == target_disk[1]:
            return False
            
        return True

    
    """
    Move a disk from source to target
    
    Args:
        source (str): The source tower ('A', 'B', or 'C').
        target (str): The target tower ('A', 'B', or 'C').
    
    Returns:
        bool: True if the move was successful, False otherwise.
        
    """
    def move_disk(self, source, target):
        if self.is_valid_move(source, target):
            disk = self.towers[source].pop()
            self.towers[target].append(disk)
            self.moves.append((disk[0], source, target))
            return True
        return False

"""

Solve the Tower of Hanoi puzzle with the color rule.

Args:
    n (int): Number of disks in the puzzle.
    disks (list): List of tuples where each tuple contains (size, color).
                  The disks should be ordered from largest to smallest.
                  
    Returns:
        list: List of moves to solve the puzzle.
        int: Number of moves to solve the puzzle.
        -1: If the puzzle is impossible to solve.
        
"""

def solve_hanoi(n, disks):
    game = ColorHanoi(disks)
    
    def hanoi_recursive(n, source, auxiliary, target, game):
        if n == 0:
            return True
            
        # Try moving n-1 disks to auxiliary
        if not hanoi_recursive(n-1, source, target, auxiliary, game):
            return False
            
        # Move nth disk to target
        if not game.move_disk(source, target):
            return False
            
        # Move n-1 disks from auxiliary to target
        if not hanoi_recursive(n-1, auxiliary, source, target, game):
            return False
            
        return True

    # Try to solve
    if hanoi_recursive(n, 'A', 'B', 'C', game):
        return game.moves
    return -1

# Example usage
if __name__ == "__main__":

    # Caso 1: Caso básico con 3 discos (debe ser posible)
    print("\n=== Test Case 1: Basic case with 3 disks ===")
    n1 = 3
    disks1 = [(3, "red"), (2, "blue"), (1, "red")]
    result1 = solve_hanoi(n1, disks1)
    print(f"Result: {result1}")

    # Caso 2: Caso imposible - todos del mismo color
    print("\n=== Test Case 2: Impossible case - all same color ===")
    n2 = 3
    disks2 = [(3, "red"), (2, "red"), (1, "red")]
    result2 = solve_hanoi(n2, disks2)
    print(f"Result: {result2}")  # Should return -1

    # Caso 3: Caso límite - un solo disco
    print("\n=== Test Case 3: Edge case - single disk ===")
    n3 = 1
    disks3 = [(1, "blue")]
    result3 = solve_hanoi(n3, disks3)
    print(f"Result: {result3}")

    # Caso 4: Caso máximo - 8 discos alternando colores
    print("\n=== Test Case 4: Maximum case - 8 disks alternating colors ===")
    n4 = 8
    disks4 = [
        (8, "red"), (7, "blue"), (6, "green"), (5, "red"),
        (4, "blue"), (3, "green"), (2, "red"), (1, "blue")
    ]
    result4 = solve_hanoi(n4, disks4)
    print(f"Result: {result4}")

    # Caso 5: Caso con todos los discos de diferentes colores
    print("\n=== Test Case 5: All different colors ===")
    n5 = 5
    disks5 = [
        (5, "red"), (4, "blue"), (3, "green"), (2, "yellow"), (1, "purple")
    ]
    result5 = solve_hanoi(n5, disks5)
    print(f"Result: {result5}")

    # Caso 6: Caso con patrón específico que podría causar bloqueo
    print("\n=== Test Case 6: Potential blocking pattern ===")
    n6 = 4
    disks6 = [(4, "red"), (3, "blue"), (2, "red"), (1, "blue")]
    result6 = solve_hanoi(n6, disks6)
    print(f"Result: {result6}")

    # Caso 7: Caso límite - número máximo de discos con patrón complejo
    print("\n=== Test Case 7: Complex pattern with maximum disks ===")
    n7 = 8
    disks7 = [
        (8, "red"), (7, "red"), (6, "blue"), (5, "blue"),
        (4, "green"), (3, "green"), (2, "yellow"), (1, "yellow")
    ]
    result7 = solve_hanoi(n7, disks7)
    print(f"Result: {result7}")

    # Caso 8: Caso con dos colores alternados
    print("\n=== Test Case 8: Two alternating colors ===")
    n8 = 6
    disks8 = [
        (6, "red"), (5, "blue"), (4, "red"),
        (3, "blue"), (2, "red"), (1, "blue")
    ]
    result8 = solve_hanoi(n8, disks8)
    print(f"Result: {result8}")

    # Caso 9: Caso con validación de entrada incorrecta
    print("\n=== Test Case 9: Invalid input validation ===")
    try:
        n9 = 3
        disks9 = [(3, "red"), (1, "blue")]  # Missing disk 2
        result9 = solve_hanoi(n9, disks9)
        print(f"Result: {result9}")
    except Exception as e:
        print(f"Expected error: {str(e)}")

    # Caso 10: Caso con discos de tamaño igual (inválido)
    print("\n=== Test Case 10: Invalid case - equal size disks ===")
    try:
        n10 = 3
        disks10 = [(3, "red"), (3, "blue"), (1, "green")]
        result10 = solve_hanoi(n10, disks10)
        print(f"Result: {result10}")
    except Exception as e:
        print(f"Expected error: {str(e)}")

    # Imprimir resumen de resultados
    print("\n=== Summary of Test Cases ===")
    all_results = [result1, result2, result3, result4, result5, 
                  result6, result7, result8]
    possible_cases = sum(1 for r in all_results if r != -1)
    impossible_cases = sum(1 for r in all_results if r == -1)
    print(f"Total test cases: {len(all_results)}")
    print(f"Possible solutions: {possible_cases}")
    print(f"Impossible cases: {impossible_cases}")

