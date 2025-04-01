from inspect import currentframe, getframeinfo

#prints in console the function and source line number where the function is called
def debug(m):
    f=getframeinfo(currentframe().f_back)
    print(">["+f.function+"@"+str(f.lineno)+"] "+m)
