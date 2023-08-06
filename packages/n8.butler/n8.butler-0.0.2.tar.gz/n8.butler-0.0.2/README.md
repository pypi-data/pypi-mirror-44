# Butler 0.0.2
It just works. This is basically just a random package.

## Shorten big numbers
Starts shortening at thousand and stops at trillion.
```python
from butler import numbers
numbers.shorten(10000000)
```
Outputs: 10M

## Countdowns
Countdown to day and hour
```python
from butler import countdown
countdown.day_and_hour('monday', 12)
```
Output: [days, hours, minutes, seconds]

Countdown to hour
```python
from butler import countdown
countdown.hour(12)
```
Ouput: [hours, minutes, seconds]