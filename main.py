import os
import time
import json
import configparser
from random import randint

def is_archer(grid, row, col):
    return True if grid[row][col] == 'A' else False

def is_wall(grid, row, col):
    return True if grid[row][col] == 'W' else False

def check_horizontal(grid, k, w, row, col):
    if col == 0:
        return True
    
    start_col = col - 1
    temp_col = start_col
    while w > 0 and temp_col >= 0:
        if is_wall(grid, row, temp_col):
            return True
        if is_archer(grid, row, temp_col):
            return False
        temp_col -= 1
        w -= 1

    return True

def check_vertical(grid, k, w, row, col):
    if row == 0:
        return True
    
    start_row = row - 1
    temp_row = start_row
    while w > 0 and temp_row >= 0:
        if is_wall(grid, temp_row, col):
            return True
        if is_archer(grid, temp_row, col):
            return False
        temp_row -= 1
        w -= 1

    return True

def check_main_diagonal(grid, k, w, row, col):
    if row == 0 or col == 0:
        return True
    
    start_row = row - 1
    start_col = col - 1
    temp_row = start_row
    temp_col = start_col
    while w > 0 and temp_row >= 0 and temp_col >= 0:
        if is_wall(grid, temp_row, temp_col):
            return True
        if is_archer(grid, temp_row, temp_col):
            return False
        temp_row -= 1
        temp_col -= 1
        w -= 1

    return True

def check_secondary_diagonal(grid, k, w, row, col):
    if row == 0 or col == k - 1:
        return True
    
    start_row = row - 1
    start_col = col + 1
    temp_row = start_row
    temp_col = start_col
    while w > 0 and temp_row >= 0 and temp_col < k:
        if is_wall(grid, temp_row, temp_col):
            return True
        if is_archer(grid, temp_row, temp_col):
            return False
        temp_row -= 1
        temp_col += 1
        w -= 1

    return True

def is_valid(grid, k, w, row, col):
    if row < 0 or col < 0 or row >= k or col >= k:
        return False
    
    if is_archer(grid, row, col):
        return False
    
    if is_wall(grid, row, col):
        return False
    
    if not check_horizontal(grid, k, w, row, col):
        return False
    
    if not check_vertical(grid, k, w, row, col):
        return False
    
    if not check_main_diagonal(grid, k, w, row, col):
        return False
    
    if not check_secondary_diagonal(grid, k, w, row, col):
        return False

    return True
    

def dfs(grid, n, k, w, row = 0, col = 0) -> bool:
    if n == 0:
        return True
    
    if col == k:
        row += 1
        col = 0
        if row == k:
            return False
    
    if is_valid(grid, k, w, row, col):
        grid[row][col] = 'A'
        if dfs(grid, n - 1, k, w, row, col + 1):
            return True
        grid[row][col] = '.'
    
    return dfs(grid, n, k, w, row, col + 1)

def remove_tests_and_results():
    '''This function will make sure that there are no remaining tests
    and results before the generation of new tests starts.'''
    tests_path = os.getcwd() + '\\tests\\'
    results_path = os.getcwd() + '\\results\\'
    for file in os.listdir(tests_path):
        file_path = tests_path + file
        os.remove(file_path)

    for file in os.listdir(results_path):
        file_path = results_path + file
        os.remove(file_path)

def fetch_configuration_values():
    '''This function will get the configuration values for the test generator
    present in the 'config.ini' file present in the project'''

    remove_tests_and_results()

    config = configparser.ConfigParser()
    config.read('config.ini')
    min_grid_length, max_grid_length = (int(config.get('GENERATION VALUES', 'MIN_GRID_LENGTH')), int(config.get('GENERATION VALUES', 'MAX_GRID_LENGTH')))
    min_archers, max_archers = (int(config.get('GENERATION VALUES', 'MIN_ARCHERS')), int(config.get('GENERATION VALUES', 'MAX_ARCHERS')))
    min_archer_strength, max_archer_strength = (int(config.get('GENERATION VALUES', 'MIN_ARCHER_STRENGTH')), int(config.get('GENERATION VALUES', 'MAX_ARCHER_STRENGTH')))
    min_walls_nmb, max_walls_nmb = (int(config.get('GENERATION VALUES', 'MIN_WALLS_NMB')), int(config.get('GENERATION VALUES', 'MAX_WALLS_NMB')))
    test_nmb = int(config.get('GENERATION VALUES', 'TESTS'))
    config_dict = {
        'min_grid_length' : min_grid_length,
        'max_grid_length' : max_grid_length,
        'min_archers' : min_archers,
        'max_archers' : max_archers,
        'min_archer_strength' : min_archer_strength,
        'max_archer_strength' : max_archer_strength,
        'min_walls_nmb' : min_walls_nmb,
        'max_walls_nmb' : max_walls_nmb,
        'test_nmb' : test_nmb
    }
    return config_dict, test_nmb

def test_generator(config_dict, test_no):
        '''This function will take some configuration info for the limits of the
        parameters of the test generation from the configuration file and generate
        a specific number of tests.'''

        test_path = os.getcwd() + '\\tests\\'
        result_path = os.getcwd() + '\\results\\'
        test_name = f'test{str(test_no)}.json'
        result_name = f'result{str(test_no)}.json'

        length = randint(config_dict['min_grid_length'], config_dict['max_grid_length'])
        archers = randint(config_dict['min_archers'], config_dict['max_archers'])
        strength = randint(config_dict['min_archer_strength'], config_dict['max_archer_strength'])
            
        if config_dict['max_archers'] > length:
            archers = randint(config_dict['min_archers'], length)

        walls_nmb = randint(config_dict['min_walls_nmb'], config_dict['max_walls_nmb'])
        if config_dict['max_walls_nmb'] > (length ** 2):
            walls_nmb = randint(config_dict['min_walls_nmb'], length ** 2)
            
        grid = [['.' for _r in range(length)] for _c in range(length)]
        for _ in range(walls_nmb):
            loop_wall = True
            while(loop_wall):
                temp_wall = randint(0, length ** 2 - 1)
                _row = temp_wall % length
                _col = temp_wall // length
                if grid[_row][_col] == '.':
                    loop_wall = False
                    grid[_row][_col] = 'W'

        test_dict = {
            'length' : length,
            'archers' : archers,
            'strength' : strength,
            'grid' : grid
        }

        result_dict = {
            'length' : length,
            'archers' : archers,
            'strength' : strength, 
        }

        problem_test_path = test_path + test_name
        problem_result_path = result_path + result_name
            
        with open(problem_test_path, 'w') as file:
            json.dump(test_dict, file, indent = 4)

        return (length, archers, strength, grid, problem_test_path, problem_result_path, result_dict)

def print_solution(k, initial_grid, result_grid):
    length = k
    sign_grid = list()
    row_number = int()
    internal_log = ''
    if length % 2:
        row_number = [length // 2]
        row_arrow = ['  ---|>  ']
    else:
        row_number = [((length // 2) - 1), (length // 2)]
        row_arrow = ['  ---|\  ', '  ---|/  ']

    for index in range(length):
        if index in row_number:
            arrow_index = row_number.index(index)
            sign_grid.append(row_arrow[arrow_index])
        else:
            sign_grid.append('         ')

    for initial_row, sign_row, final_row in zip(initial_grid, sign_grid, result_grid):
        internal_log += f'{initial_row} {sign_row} {final_row}\n'

    return internal_log

def main():
    config_dict, no_tests = fetch_configuration_values()
    log = ''
    start_time = time.perf_counter() * 1000
    for test in range(no_tests):
        t_start_time = time.perf_counter() * 1000

        test_values = test_generator(config_dict, test)
        test_path, result_path = test_values[4], test_values[5]
        (k, n, w, grid) = test_values[0], test_values[1], test_values[2], test_values[3]
        result_dict = test_values[6]

        t_end_time = time.perf_counter() * 1000
        t_elapsed_time = t_end_time - t_start_time
        log += f'The values for test no. {str(test)} were generated in {t_elapsed_time:.2f} milliseconds!\n'

        log += f'For test no. {str(test)} @ {test_path}\nk : {k}, n : {n}, w : {w}\n'
        start_grid = [row[:] for row in grid]
        e_start_time = time.perf_counter() * 1000

        solution_found = dfs(grid, n, k, w)
        e_end_time = time.perf_counter() * 1000
        e_elapsed_time = e_end_time - e_start_time

        if solution_found:
            log += f'The solution for test no. {str(test)} was found in {e_elapsed_time:.2f} milliseconds!\n'
        else:
            log += f'The solution for test no. {str(test)} was NOT found in {e_elapsed_time:.2f} milliseconds!\n'
            
        result_dict['solution'] = grid
        with open(result_path, 'w') as file:
            json.dump(result_dict, file, indent = 4)

        log += print_solution(k, start_grid, grid) + '\n'  
    
    end_time = time.perf_counter() * 1000
    elapsed_time = end_time - start_time
    log += f'The program ended successfully in {elapsed_time:.2f} milliseconds!\n'

    with open('_execution.log', 'w') as f:
        f.write(log)

if __name__ == '__main__':
    main()