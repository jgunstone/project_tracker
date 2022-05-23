import glob
import pandas as pd
import os
import fnmatch

def find_in_list(li, string):
    '''
    searches list for string and returns matching
    Code:
        return [s for s in li if string in s]
    '''
    return [s for s in li if string in s]
 
def recursive_glob(rootdir='.', pattern='*', recursive=True):
    """ 
    Search recursively for files matching a specified pattern.
    
    Reference: 
        Adapted from: http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
        string pattern matching: https://jakevdp.github.io/WhirlwindTourOfPython/14-strings-and-regular-expressions.html
    Args:
        **rootdir (string): the directory that you would like to recursively search. 
            recursive means it will automatically look in all folders within this directory
        **pattern (string): the filename pattern that you are looking for.
        **recursive (bool): define if you want to search recursively (in sub-folders) or not. 
        
    Returns:
        matches(list): list of filedirectories that match the pattern
    Example:
        rootdir='J:\J'+'J9999'
        pattern='????????_????_?*_?*_?*_?*_?*_?*'
        recursive_glob(rootdir=rootdir, pattern=pattern, recursive=True)
    """
    matches=[]
    if recursive ==True:
        for root, dirnames, filenames in os.walk(rootdir):
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
    else:
        for filename in glob.glob1(rootdir,pattern):
            matches.append(os.path.join(rootdir,filename))
    return matches


def highlight_row(s, di,col):
    '''
    pass a dict and the column to match value to colour row as per
    the dict based on the column value passed. 

    Example:
        colours={'Project Management':'background-color: #afbaff',
                'Engineering Analysis':'background-color: #f9b8b8',
                'Engineering Design':'background-color: #bfffc2',
                'Backend Development':'background-color: #e5baff',
                'Frontend Development':'background-color: #fbfcb8'}

        if highlight_row == True:
        display((df2.style
        .apply(highlight, di=colours, col=['WorkType'], axis=1)
        .format({'Budget': '£{:,.0f}'})
            ))
        else:
        display((df2.style
        .applymap(highlight_cell,di=colours,subset=['WorkType'])
        .format({'Budget': '£{:,.0f}'})
            ))
    '''
    is_val = pd.Series(data=False, index=s.index)
    is_val[col] = s.loc[col] 
    return [di[is_val.WorkType] if is_val.WorkType in list(di.keys()) else '' for v in is_val]

def highlight_cell(value,di):
    '''
    pass a value and a dict which colours cells based on values

    Example:
        colours={'Project Management':'background-color: #afbaff',
                'Engineering Analysis':'background-color: #f9b8b8',
                'Engineering Design':'background-color: #bfffc2',
                'Backend Development':'background-color: #e5baff',
                'Frontend Development':'background-color: #fbfcb8'}

        if highlight_row == True:
        display((df2.style
        .apply(highlight, di=colours, col=['WorkType'], axis=1)
        .format({'Budget': '£{:,.0f}'})
            ))
        else:
        display((df2.style
        .applymap(highlight_cell,di=colours,subset=['WorkType'])
        .format({'Budget': '£{:,.0f}'})
            ))
    '''
    li = list(di.keys())
    if value in li:
        colour = di[value]
    else:
        colour = 'background-color: white'
    return colour