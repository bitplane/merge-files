from pydantic import constr

_decimal = r"""
    \d+            # At least one digit
    (              # subgroup
        _          #   an underscore
        \d+        #   at least one digit
    )*             # zero or more times
    [l|L]?         # Optional long
"""

_hexadecimal = r"""
    0x             # Hexadecimal prefix
    [0-9a-fA-F]+   # At least one hexadecimal digit
    (              # subgroup
        _          #   an underscore
        [0-9a-fA-F]+ # at least one hexadecimal digit
    )*             # zero or more times
"""

_octal = r"""
    0o             # Octal prefix
    [0-7]+         # At least one octal digit
    (              # subgroup
        _          #   an underscore
        [0-7]+     #   at least one octal digit
    )*             # zero or more times
"""

_binary = r"""
    0b             # Binary prefix
    [01]+          # At least one binary digit
    (              # subgroup
        _          #   an underscore
        [01]+      #   at least one binary digit
    )*             # zero or more times
"""

_integer = rf"""
    (
    \s*                    # Optional whitespace
    [+-]?                  # Optional sign
    {_decimal}             # Decimal integer
    |                      # or
    {_hexadecimal}         # Hexadecimal integer
    |                      # or
    {_octal}               # Octal integer
    |                      # or
    {_binary}              # Binary integer
    )
"""

_zero_integer = "(0[xob])?0+"

_nonzero_integer = rf"""((!{_zero_integer}){_integer})"""

integer_regex = rf"""(?x)  # Verbose regex
    ^                      # start of string
    {_integer}
    $                      # End of string
"""

nonzero_integer_regex = rf"""(?x)  # Verbose regex
    ^                              # start of string
    {_nonzero_integer}
    $                              # End of string
"""

_range = rf"""
    (!$|\s+$|\s*,|\s*,\s*$)          # Not empty
    (
        {_integer}?                  # Start of range
        (
            \:?                      # Colon
            {_integer}?              # End of range
            (
                \:?                  # Colon
                {_nonzero_integer}?  # Step
            )?
        )?
        \s*                          # Optional whitespace
    )
"""

range_regex = rf"""(?x)  # Verbose regex
    ^                    # start of string
    {_range}             # Range
    $                    # End of string
"""

ranges_regex = rf"""(?x) # Verbose regex
    ^                    # start of string
    {_range}             # Range
    (                    # subgroup
        \s*              #   Optional whitespace
        ,                #   Comma
        \s*              #   Optional whitespace
        {_range}         #   Range
    )*                   # zero or more times
    $                    # End of string
"""

Integer = constr(regex=integer_regex)
# Range = constr(regex=range_regex)
# Ranges = constr(regex=ranges_regex)
