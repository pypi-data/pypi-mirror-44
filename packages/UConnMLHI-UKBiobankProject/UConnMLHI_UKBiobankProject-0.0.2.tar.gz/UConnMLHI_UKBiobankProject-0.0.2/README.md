# UConnMLHI_UKBiobankProject


## Installation
### Installation via pip (Not done yet)
* For local installation
```
    $ pip install UConnMLHI_UKBiobankProject --user
```

* For global installation
```
    $ sudo pip install UConnMLHI_UKBiobankProject
```
### Manual Installation
```
    $ git clone https://github.com/xinyuwang1209/UConnMLHI_UKBiobankProject
    $ cd UConnMLHI_UKBiobankProject
```
* For local installation
```
    $ python setup.py install --user
```

* For global installation
```
    $ sudo python setup.py install
```


## Usage
### Get the module
``` 
    from UConnMLHI_UKBiobankProject import *
    Instance = UConnMLHI_UKBiobankProject()
```

### Data_Process
#### Run dta2csv
* Set return_df = True, if you want to get the dataframe file beside saving it in csv
```    
    df = Instance.Data_Process.dta2csv('/path/to/file',return_df=True)
```

* Set return_df = False if you only want to save the data into csv format
```
    Instance.Data_Process.dta2csv('/path/to/file',return_df)
```
