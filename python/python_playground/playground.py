"""
" A 'playground' to familiarize myself with the python language
" Dabbled in DataFrames and numpy arrs as well
" No real goal or target to this file.
"""

import numpy as np
import pandas as pd


def quicksort(arr):
    print('\nfunction start with arr=')
    print(arr)
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    print(left, middle, right)
    print('function end')
    return quicksort(left) + middle + quicksort(right) #recursive call for left and right elements of pivot
#print(quicksort([3,6,8,10,1,2,1]))

def basic_data_types():
    x = 3
    s = 'string'
    print('x=3, printing x')
    print (x)

    print('\nprinting type(x)')
    print(type(x))

    
    print('\nplaying with negative index in an array- [-1]')
    int_arr = [9,8,7,6,5,4,3,2,1,0]
    print(int_arr)
    print(int_arr[-1])
    print('-1 index is the last element in the arr')

    print('\npython arrs are not limited to a single type. append \'nine\' using .append')
    int_arr.append('nine')
    print(int_arr)

    print('\n similar to cpp vector, pop can be used on arr to retyrn and remove last element of the list')
    print(int_arr.pop())
    print(int_arr)

    print('\nsupport of slicing arrs are included ex: [0:2]')
    print(int_arr[0:2]) #index 0 to index 2 exclusive (up to but not including element 2)
    
    print('\ncan leave out an argument to shorthand ex [:3]')
    print(int_arr[:3]) #automatically assumes from index 0

    print('\nif a negative arg is used, it depends on the args loc')
    print('ex: [-3:] means first 3 elements')
    print(int_arr[-3:]) 
    print('\nex: [:-3] means all but last 3 elements')
    print(int_arr[:-3]) 
    
    print('\nyou can iterate through arr directly')
    for elements in int_arr:
        print(elements)

    print('\nan interesting function called enumerate')
    str_arr = ['a','b','c','d','e','f','g','h']
    for count, elements in enumerate(str_arr):
        print(count, elements)

    print('\nyou can also specify the starting index of the counter')
    for count, elements in enumerate(str_arr, 99):
        print(count, elements)

    print('\nyou can also use it to create tuples directly')
    enum_tuple = list(enumerate(str_arr,1))
    print(enum_tuple)

    print('\nbut requires the use of the list() function that returns a list of the iterable object')
    t_list = [9,8,7]
    print('printing t_list vs list(t_list')
    print(t_list)
    print(list(t_list))
# basic_data_types()

def series_play():
    # Series(what to initialize as, index=the rows in the series)
    series = pd.Series(
    np.random.randn(4),
    index=['a','b','c','d'],
    name='example')

    print('\nprinting series')
    print(series)

    print('\nprinting series[0]')
    print(series[0])    #indexing the first, in this case 'a'

    print('\nprinting series.values')
    print(series.values)    #numpy array of all the values in the indexies

    print('\nprinting series slice by indexies')
    print(series[[2,1,3]])  #prints 2='c' 1='b' 3='d'

    print('\nprinting map/dictionary like indexing')
    print(series['a'])  #prints the value at 'index' 'a'

    print('\ncan use the above to mutate values')
    series['a']=99 
    print(series)

    print('\ncan broadcast through series depending on conditional')
    print(series > 0.5)

    print('\nnow use the result of the conditional to show only the true\'s')
    print(series[series > 0.5])

def df_play():
    print('\nnow we play with the check_state_exist located in RL_brain.py')
    print('lets start with setting action space and init q_table')
    actions = ['U','D','L','R']
    q_table = pd.DataFrame(columns=actions, dtype=np.float64)

    print('\nactions = %s' % str(actions))
    print('q_table:')
    print(q_table)

    print('##################################')

    print('trying my hand at daraframe')
    data = {'Position':  ('xpos','ypos'),
            'Values': ['U', 'D', 'L', 'R'],
            }
    df = pd.DataFrame (columns = actions, dtype = np.float64)
    print('\nprinting df')
    print (df)

    print('\nappending to df table')
    state = 'test_state'
    df = df.append(
        pd.Series(
            [0]*len(actions),
            index=df.columns,
            name=state,)
    )
    print('printing df with appended')
    print (df)

    print('\ntesting appending a Series type with name (int, int)')
    coords = (0,0)
    print(type(coords))
    df = df.append(
        pd.Series(
            [0, 1, 2, 3],
            index=df.columns,
            name=str(coords),
        )
    )
    print (df)

    print('##################################')
    print('test append worked so gonna try indexing from the name')
    print('\nis \'test_state\' in df.index?')
    print('test_state' in df.index)

    print('is coords aka(0,0) in df.index?')
    print(coords in df.index)
    print('is 99 in df.index?')
    print(99 in df.index)

    print('\n##################################')
    print('now finding the max of a entry in the dataframe')
    print(df)

    print('return list of elements in coords(0,0)')
    action_choices = df.loc[str(coords),:]
    print(action_choices)


df_play()

print(int('a',16))
print(int('b',16))
print(int('a',16)-1)
print(int(0))

