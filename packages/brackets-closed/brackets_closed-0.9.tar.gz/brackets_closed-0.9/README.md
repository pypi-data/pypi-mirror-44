# bracket_closed

## Checks if all brackets in a string are balanced

## Example code:

```
from brackets_closed import close_check

close_check.is_closed("([])")
close_check.is_closed("([)]")
close_check.is_closed("[](){{{{[]}}}}")
close_check.is_closed("][][")
close_check.is_closed("print('This(is) a test to see { if this code { will extract }} brackets [] fro[m a string] that is not {} just brackets!')")
```

## Output from example:

```
True
False
True
False
True
```