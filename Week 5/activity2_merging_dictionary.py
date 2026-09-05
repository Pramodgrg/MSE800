# Week 5 - Activity 2: Merging Dictionaries with Conditions
# Use the following lists as keys and values. Generate a dictionary output by selecting the key–value pairs where the value is an odd number.
# Key1:[a, b, c, d, f, g, h, e, a]
# Value1:[20, 3, 1, 88, 55, 92, 6, 90, 910]
# Key2:[u, b, o, x,  e, a]
# Value2:[200, 30, 10, 88, 55, 920]
# Share your code and the resulting output here with description.



Key1 =['a', 'b', 'c', 'd', 'f', 'g', 'h', 'e', 'a']
Value1 = [20, 3, 1, 88, 55, 92, 6, 90, 910]
Key2 =['u', 'b', 'o', 'x',  'e', 'a']
Value2 = [200, 30, 10, 88, 55, 920]

dict1 = {k:v for k,v in zip(Key1,Value1) if v%2 != 0}
dict2 = {k:v for k,v in zip(Key2, Value2) if v%2 != 0}

merged_dict = {**dict1, **dict2}

print (merged_dict)
 
 