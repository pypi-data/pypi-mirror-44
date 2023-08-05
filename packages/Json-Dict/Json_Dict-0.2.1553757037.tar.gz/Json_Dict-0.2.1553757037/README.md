A self saving json based config file.
Storable data are all classical JSON datatypes including lists/arrays and dictionaries, which will be stored as JSON Objects.

The Json_Dict object can be initalized via `jd = JsonDict()`

The Object can be initalized with a file (as path) , which will be
created if not existend (turn off by passing `createfile=False` as parameter).
You can also pass initial data to the instance via the `data`. The data can be in the form of another JsonDict, an JSON string or an JSON serializable dictionary.
If a file is specified the JsonDict will first try to read the file and if this does not work fall back to the initial provided data.

If a file is provided the JsonDict will be saved to the file on value addition/change. This can be turned of generally 
by providing the initial argument `autosave=False` or setting the `autosave` attribute to False any time.
For not saving at a specific request you can also pass the `autosave=False` parameter to a get or put request.

path_to_file content: {"a":1,"b":{"c":"foo","d":100},"d":["bar",0.1]}  
`jd = JsonDict(file=path_to_file, creatfile=False, autosave=False)`  
will generate a JsonDict initalized with the file content but never overwrites it unless `js.save()` is called. If autosave is not passed during initalization or set to True every change to the JsonDict will be saved directly to the file.

The call `jd = JsonDict(file=path_to_invalif_file,data={'a':1}, creatfile=False, autosave=False)`
will initalize the object with with the data provided by the data parameter since the file is invalid and not created during initalization


The data in the JsonDic object is set via the `jd.put("key","subkey","subsubkey",...,value=value)`.
where all the args are used as keys to the value which is set by the value kwarg.  
In this manner `js.put("b","c",value="foo")` will change a JsonDict with the data`{'a':1}` to `{'a':1,'b':{'c':'foo'}}`  
Keep in mind that every type can be used as a key but it will be transformed to the corresponding string representation!

To get the data from the JsonDict you can use `jd.put("key","subkey","subsubkey",...,default=defaultvalue)` respectively.
The optional default parameter can be used to set the value if the keystructure is not present in the dict otherwise None will be returned.
The requested structure will be saved in the JsonDict whether or not it is already present or not!

