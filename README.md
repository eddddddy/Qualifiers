# Qualifiers
## About
Contains decorators to specify visibility of Python methods. `AttributeError` is thrown whenever a method is illegally accessed or overidden. Semantics are identical to Java.

Does this truly mask visibility? No. You can still access the methods if you *really* wanted to. But if you were trying to bypass it, why use it in the first place?

Is this tested? Barely. 

Is this Pythonic? Of course not. 

Should this be used? Probably not.

## Installation
All you need is the standalone qualifiers.py file. Clone the repo or manually download it.

## Usage
```python
from qualifiers.py import qualify, private, protected, public, final

@qualify
class Test:

	@private
	def private_method(self):
		print("Private")
		
	@protected
	def protected_method(self):
		print("Protected")
	
	@public
	def public_method(self):
		print("Public")

	@final
	def final_method(self):
		print("Final")

	@private
	@final
	def private_final_method(self):
		print("Private final")
```
