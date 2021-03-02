# Python-Microblocks

# Explanation
This module is created in order to make it simple
and easier to run functions in parallel or in sequential.

# Usage
If you wish to run functions in parallel, call the function:
`start_parallel` when the first parameters is 
iterable data structure (like tuple or list) 
which contain the function's pointers.
And the second argument is also iterable data structure
of tuples, when each tuple will contain the arguments
for each function. if there is no argument for specific function,
pass empty tuple. The location of the tuples and the function's pointer
need to be the same.
If you wish to run functions in sequential, call the function
named `start_sequential` with the same arguments as the 
`start_parallel` function. 
