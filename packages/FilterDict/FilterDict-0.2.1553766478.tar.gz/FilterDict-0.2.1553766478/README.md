A simple function to generate a simple filtered dict where a dict is created based on a dictionary and a function.
The returned dict contains all the kwargs if the passed function which are present in the inut dict.  
This is espacially useful if you have a dict with more keys than needed to call a function or you call a function by reference and want to pass an dict as kwargs

Example:  
```
d = dict(a=0,b=1,s1="foo",s2="bar") 
def merge_strings(s1="",s2=""):
    return s1+s2
    
print(merge_strings(**d))
#throws TypeError: merge_strings() got an unexpected keyword argument 'a'

print(merge_strings(**filter_dict(d,merge_strings)))
# returns foobar as expected

```
