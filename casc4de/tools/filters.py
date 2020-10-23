# from casc4de import app

# @app.template_filter("is_float")
def is_float(value):
    """
        Command to parse                        Is it a float?  Comment
    --------------------------------------  --------------- ------------
    print(isfloat(""))                      False
    print(isfloat("1234567"))               True 
    print(isfloat("NaN"))                   True            nan is also float
    print(isfloat("NaNananana BATMAN"))     False
    print(isfloat("123.456"))               True
    print(isfloat("123.E4"))                True
    print(isfloat(".1"))                    True
    print(isfloat("1,234"))                 False
    print(isfloat("NULL"))                  False           case insensitive
    print(isfloat(",1"))                    False           
    print(isfloat("123.EE4"))               False           
    print(isfloat("6.523537535629999e-07")) True
    print(isfloat("6e777777"))              True            This is same as Inf
    print(isfloat("-iNF"))                  True
    print(isfloat("1.797693e+308"))         True
    print(isfloat("infinity"))              True
    print(isfloat("infinity and BEYOND"))   False
    print(isfloat("12.34.56"))              False           Two dots not allowed.
    print(isfloat("#56"))                   False
    print(isfloat("56%"))                   False
    print(isfloat("0E0"))                   True
    print(isfloat("x86E0"))                 False
    print(isfloat("86-5"))                  False
    print(isfloat("True"))                  False           Boolean is not a float.   
    print(isfloat(True))                    True            Boolean is a float
    print(isfloat("+1e1^5"))                False
    print(isfloat("+1e1"))                  True
    print(isfloat("+1e1.3"))                False
    print(isfloat("+1.3P1"))                False
    print(isfloat("-+1"))                   False
    print(isfloat("(1)"))                   False           brackets not interpreted
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

# @app.template_filter('reverse')
# def reverse_filter(s):
#     return s[::-1]