def table_to_xyz(dataframe):
    """
    This function transforms a given dataframe into a new dataframe with three columns: 'X', 'Y', and 'Z'.
    The 'X' values are taken from the first column of the input dataframe.
    The 'Y' values are the headers of the subsequent columns of the input dataframe, converted to floats.
    The 'Z' values are the corresponding values from the input dataframe for each 'X' and 'Y'.
    
    Parameters:
    dataframe (pd.DataFrame): The input dataframe to be transformed. The first column is used for 'X' values,
                              and the headers of the subsequent columns are used for 'Y' values.
    
    Returns:
    new_dataframe (pd.DataFrame): The resulting dataframe with columns 'X', 'Y', and 'Z'.
    """
    headers = dataframe.columns[1:]
    new_data = []

    for index, row in dataframe.iterrows():
        x_value = row[dataframe.columns[0]] # using the first column as x_value
        for header in headers:
            y_value = float(header)
            z_value = row[header]
            new_row = {'X': x_value, 'Y': y_value, 'Z': z_value}
            new_data.append(new_row)
    
    new_dataframe = pd.DataFrame(new_data)
    return new_dataframe

def dict_zip(*dicts):
    """
    This function takes in an arbitrary number of dictionaries and combines them 
    into a single dictionary. Each key in the output dictionary has a list of 
    associated values from each input dictionary where the key exists.
    
    Parameters:
    ------------
    *dicts : dict
        An arbitrary number of dictionaries to be combined. 

    Returns:
    -----------
    dict
        A dictionary with each key from the input dictionaries and 
        its corresponding values in a list. If a key does not exist 
        in an input dictionary, it is not included in the list of values 
        for that key in the output dictionary.

    Example:
    --------
    >>> dict1 = {'a': 1, 'b': 2}
    >>> dict2 = {'b': 3, 'c': 4}
    >>> dict3 = {'a': 5, 'c': 6}
    >>> dict_zip(dict1, dict2, dict3)
    {'a': [1, 5], 'b': [2, 3], 'c': [4, 6]}
    """
    all_keys = {k for d in dicts for k in d.keys()}
    return {k: [d[k] for d in dicts if k in d] for k in all_keys}


def dict_extract(key, var):
    """
    This function traverses through a dictionary (also capable of handling nested dictionaries and lists) 
    and yields the values associated with the specified key.

    This function uses a generator, so it doesn't return all values at once, 
    but generates them on the fly. This is useful for large structures as it saves memory.
    
    Parameters:
    ------------
    key : str
        The key to be searched in the dictionary.

    var : dict or list
        The dictionary or list in which the search is to be made. This function can 
        handle nested dictionaries and lists.
    
    Yields:
    -------
    var_type : type of the value
        The value from the dictionary associated with the key. 
        The type of value depends on the dictionary.

    Example:
    --------
    >>> data = {
        'id': 1, 
        'info': {
            'name': 'John', 
            'contacts': [
                {'type': 'phone', 'value': '555-555-555'}, 
                {'type': 'email', 'value': 'john@mail.com'}
            ]
        }
    }
    >>> gen = dict_extract('value', data)
    >>> list(gen)
    ['555-555-555', 'john@mail.com']
    """
    if hasattr(var,'items'): 
        for k, v in var.items(): 
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in dict_extract(key, d):
                        yield result
            else:
                pass

def dict_flatten2(my_dict, separator="/", concat_key="", new_dict=None):
    """
    Flattens a nested dictionary into a single-level dictionary.

    This function recursively traverses the input dictionary, concatenating the keys of nested dictionaries 
    with the provided 'separator' to create new keys for the flattened dictionary.

    Parameters:
    my_dict (dict): The dictionary to flatten.
    separator (str, optional): The string used to separate nested dictionary keys. Defaults to "/".
    concat_key (str, optional): The initial string to concatenate to the keys. Defaults to "".
    new_dict (dict, optional): An existing dictionary to add the flattened keys and values to. If not provided,
                               a new dictionary is created.

    Returns:
    dict: The flattened dictionary.

    Example:
    >>> my_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
    >>> dict_flatten(my_dict, separator=".")
    {'a': 1, 'b.c': 2, 'b.d.e': 3}
    """
    if new_dict is None:
        new_dict = dict()
    keys = my_dict.keys()
    for key in keys:
        new_concat_key = concat_key + key if concat_key == "" else concat_key + separator + key
        if isinstance(my_dict[key], dict):
            dict_flatten(my_dict[key], separator=separator, concat_key=new_concat_key, new_dict=new_dict)
        else:
            new_dict[new_concat_key] = my_dict[key]
    return new_dict

def dict_unflatten2(flat_dict, separator="/"):
    """
    Unflattens a flat dictionary into a nested dictionary.

    This function traverses the input dictionary, splitting the keys at each instance of the 'separator' 
    and creates new nested dictionaries for each split part of the key.

    Parameters:
    flat_dict (dict): The flat dictionary to unflatten.
    separator (str, optional): The string used to separate parts of the keys in the flat dictionary. Defaults to "/".

    Returns:
    dict: The unflattened (nested) dictionary.

    Example:
    >>> flat_dict = {'a': 1, 'b.c': 2, 'b.d.e': 3}
    >>> dict_unflatten(flat_dict, separator=".")
    {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
    """
    nested_dict = {}
    for key, value in flat_dict.items():
        curr_dict = nested_dict
        split_key = key.split(separator)
        for sub_key in split_key[:-1]:
            curr_dict = curr_dict.setdefault(sub_key, {})
        curr_dict[split_key[-1]] = value
    return nested_dict
           
def dict_flatten(my_dict, concat_key="", new_dict=None):
    if new_dict is None:
        new_dict = dict()
    keys = my_dict.keys()
    for key in keys:
        if isinstance(my_dict[key], dict):
            dict_flatten(my_dict[key], concat_key=concat_key + key + "/",
                        new_dict=new_dict
                        )  # Paso diccionario del siguiente nivel a la funcion
        else:
            new_dict[concat_key + key] = my_dict[key]
    return new_dict

def dict_unflatten(flat_dict):
    nested_dict = {}
    for key, value in flat_dict.items():
        curr_dict = nested_dict
        split_key = key.split("/")
        for sub_key in split_key[:-1]:
            curr_dict = curr_dict.setdefault(sub_key, {})
        curr_dict[split_key[-1]] = value
    return nested_dict

def dict_invert(my_dict):
    """
    Inverts a dictionary by swapping its keys and values.

    The function takes a dictionary as an input and creates a new dictionary where the keys 
    are the values from the input dictionary and the values are lists of keys from the input 
    dictionary that had the corresponding value.

    Parameters:
    my_dict (dict): The dictionary to invert.

    Returns:
    dict: The inverted dictionary where each key is a value from the input dictionary and 
          each value is a list of keys from the input dictionary that had the corresponding value.

    Note: 
    If the same value is shared by multiple keys in the input dictionary, then in the inverted 
    dictionary that value becomes a key associated with a list of all the keys that shared 
    that value in the input dictionary.

    Example:
    >>> my_dict = {'a': 1, 'b': 2, 'c': 2}
    >>> dict_invert(my_dict)
    {1: ['a'], 2: ['b', 'c']}
    """
    inverted_dict = dict()
    for key, value in my_dict.items():
        inverted_dict.setdefault(value, list()).append(key)
    return inverted_dict


def dict_to_html(dict_, class_name=''):
    """
    Converts a dictionary into an HTML table representation.

    This function takes a dictionary, converts it into a pandas DataFrame, and then uses the 
    pandas `to_html` method to generate an HTML table. If a class name is provided, it replaces 
    the default 'dataframe' class in the HTML string with the provided class name.

    Parameters:
    dict_ (dict): The dictionary to convert to an HTML table.
    class_name (str, optional): The class name to use for the HTML table. If not provided, 
                                the default pandas class 'dataframe' is used. 

    Returns:
    str: The HTML string representation of the dictionary.

    Note:
    The dictionary keys become the rows of the table and the dictionary values become the 
    corresponding cells in the table.

    Example:
    >>> dict_ = {'a': 1, 'b': 2, 'c': 3}
    >>> dict_to_html(dict_, class_name='my_table')
    '<table border="1" class="my_table">  <tbody>    <tr>      <th>a</th>      <td>1</td>    </tr>    <tr>      <th>b</th>      <td>2</td>    </tr>    <tr>      <th>c</th>      <td>3</td>    </tr>  </tbody></table>'
    """
    df = pd.DataFrame(dict_,index=[0])
    df = df.transpose()
    html = df.to_html(header=False)
    if class_name != '':
        html = html.replace('dataframe',class_name)
    return html


def list_duplicates(_list):
    """
    Finds duplicate items in a list.

    This function takes a list as an input and returns a list of items that appear more than once. 
    It uses the collections.Counter class to count the occurrences of each item in the list.

    Parameters:
    _list (list): The list to search for duplicates.

    Returns:
    list: A list of the items that appear more than once in the input list. 
          If there are no duplicates, an empty list is returned.

    Example:
    >>> _list = ['a', 'b', 'c', 'b', 'd', 'm', 'n', 'n']
    >>> list_duplicates(_list)
    ['b', 'n']
    """
    import collections
    return [item for item, count in collections.Counter(_list).items() if count > 1]


def list_to_html(items, list_type='ul', ul_class='', li_class=''):
    """
    Generate an HTML list from a list of items.
    
    Parameters:
    items (list): The list of items to convert.
    list_type (str): The type of HTML list to generate ('ul' for unordered, 'ol' for ordered). Default is 'ul'.
    ul_class (str): The CSS class name to apply to the list. Default is ''.
    li_class (str): The CSS class name to apply to each list item. Default is ''.
    
    Returns:
    str: A string of HTML representing the list.
    """
    if list_type not in ['ul', 'ol']:
        raise ValueError("Invalid list_type. Choose either 'ul' or 'ol'.")
        
    html = f'<{list_type} class="{ul_class}">\n'
    
    for item in items:
        html += f'  <li class="{li_class}">{item}</li>\n'
        
    html += f'</{list_type}>'
    return html

def str_clean(string, chars_to_remove):
    """
    This function removes specified characters from a string.
    
    Parameters:
    string (str): The input string to be cleaned.
    chars_to_remove (str): A string containing all characters to be removed from the input string.
    
    Returns:
    clean_string (str): The cleaned string with specified characters removed.
    """
    return string.translate({ord(i): None for i in chars_to_remove})


def str_findall(text,text_to_find):
    """
    This function finds all occurrences of a specified substring within a given string and returns their starting indices.

    Parameters:
    text (str): The string in which to search for occurrences.
    text_to_find (str): The substring to search for within the input string.

    Returns:
    allocur (list): A list of integers representing the starting indices of all occurrences of the substring within the input string.
    """
    allocur=[]
    while text.find(text_to_find)!=-1:
        ocur= text.find(text_to_find)
        allocur.append(ocur)
        text=text[ocur+1:]
    
    return allocur

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'{func.__name__} took {end - start:.6f} seconds')
        
        return result
    return wrapper