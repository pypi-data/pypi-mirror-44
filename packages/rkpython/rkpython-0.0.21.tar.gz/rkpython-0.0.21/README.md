# rkpython

## Description
This is a general use Python module.
For now, it only contains some functions to make reading and **writing to text files** easier, as well as a function that returns information for reading csv files**.
  
## Installation
Use  
```
pip install rkpython
```
  
Then import it in Python with 
```python
import rkpython as rk
```
## Functions
  
### `rk.to_txt(l, path = 'text_file.txt', overwrite = False, verbose = False)`
	
    Saves a list to a .txt file.

    --------------
    
    l : list, default is None
        List object to be saved.  
    
    path : str, default is 'text_file.txt'
        File path (with file name) you want to save to.  
    
    overwrite : bool, default is False  
        Overwrites the file if it exists.
        
    verbose : boolean, default is False
        Prints out a message if the operation was succesful
        
    --------------

    Examples :
    
    >>> rk.to_txt(var_list, './documents/vars.txt', verbose = True)
    File successfully written to ./documents/vars.txt

	
### `rk.read_txt(path = 'text_file.txt', verbose = False)`  

    Reads from a text file, saving the result as a list, where each line is one item.
    
    --------------
    
    path : str, default = 'text_file.txt'
        File path (with file name) you want to read from. Can be any type of file (.txt, .csv...)  
    
    verbose : boolean, default is False
        Prints out a message if the operation was succesful
        
    --------------

    Examples :
    
    >>> var_list = rk.read_txt('./documents/vars.txt', verbose = True)
    File successfully read from ./documents/vars.txt

	
### `rk.h_size(size)`


    Converts a size in bytes to a humanly readable size, with 1 decimal number. Input an integer, returns a string.
    
    --------------
        
    size : float, int
        Size of the object you want to convert, in bytes.
        
    --------------

    Examples :
    
    >>>  h_size(67108864)
    '64.0 Mb'
	
### `rk.get_mem(nb_objects = 10)` 
  
**Warning :** this function can't access the global variables so doesn't currently work. You can however copy the function from the source code and define it in your python session so that it will access the right variables.

    Prints out a list of the largest objects stored in memory, as well as the total memory usage of global variables. Returns a string.
    
    --------------
        
    nb_objects : int, default =  10
        Maximum number of items to be printed out.
        
    --------------

    Examples :
    
    >>> get_mem(5)
    Total usage : 25.3 Gb
    
     5 largest objects :
     _477  :  1.7 Gb
     _529  :  1.7 Gb
     _437  :  1.4 Gb
     _412  :  1.3 Gb
     _415  :  1.3 Gb
	

### `rk.csv_info(file)`

    Returns information about a csv or text file, such as the encoding and separators infered using csv's Sniffer() function.
    
    --------------
        
    file : str
        Path to the file you want to read.
        
    --------------
    
    csv_info().size :
        Returns the size of the file as a string.

    csv_info().separator :
        Returns the infered separator as a string.
        
    csv_info().quotechar :
        Returns the infered quote character as a string, defaults to ["].
        
    csv_info().encoding :
        Returns the infered encoding using chardet. Defaults to ascii.
        
    csv_info().rawdata :
        Returns a 8192 byte sample of the file, unencoded.

    csv_info().rows :
        Returns the number of rows in the csv file.        
        
    csv_info().columns :
        Returns the columns of the csv file.
            
    csv_info().parameters :
        Returns the separator, quotechar and encoding of the file to plug them in pandas or dask.        
            
    csv_info().info() :
        Prints out the main characteristics of the file.

    --------------

    Examples :
    
    >>> csv_info("table.csv").encoding
    'utf-8'
    
    >>> sep, quotechar, encoding = csv_info("table.csv").parameters
    >>> df = pandas.read_csv("table.csv", sep=sep, quotechar=quotechar, encoding=encoding)
    >>> print(sep, quotechar, encoding)
    ; " utf-8


### `rk.sql_dict(con, db_filter = '.*', table_filter = '.*', col_filter = '.*', strict=False)`

    Creates a dictionary listing all databases, tables and columns of a MySql server. Results can be filtered using regex.
    
    --------------
    
    con : SQLAlchemy connectable (engine/connection) or database string URI or DBAPI2 connection (fallback mode)
    
    db_filter : str or list of str, default is '.*'
        Filters on databases containing the specified regular expression(s).
    
    table_filter : str or list of str, default is '.*'
        Filters on tables containing the specified regular expression(s).
  
    column_filter : str or list of str, default is '.*'
        Filters on columns containing the specified regular expression(s).
        
    strict : boolean, default is False
        Returns only strict matches instead of partial matches.
        
    --------------

    Examples :
    
    >>> temp_dict = sql_dict(con = f'mysql://{user}:{pw}@{host}:{port}', col_filter = 'price')
    >>> temp_dict.keys()
    dict_keys(['products'])
    >>> temp_dict['products'].keys()
    dict_keys(['phones', 'laptops'])
    >>> temp_dict['products']['phones']
    ['price_without_tax',
     'price_with_tax']
    