# pandoc-code-attribute

Pandoc filter to add attributes to code blocks based on its class.


## Installation

First install python and python-pip.

Then use pip to install:

```
pip3 install --user pandoc-code-attribute
```


## Usage

### Example

This pandoc filter will add attributes to code blocks based on its class.

For example, it can be very useful to use different styles for different language in `listings` :

	---
	header-includes: |
		\usepackage{listings}
		
		\lstset{ % General settings
			numbers=left,
			numberstyle=\tiny
		}

		\lstdefinestyle{cpp}{ % Only for C++
			emphstyle=\color{Green}
		}

		\lstdefinestyle{python}{ % Only for Python
			emphstyle=\color{Magenta}
		}
	---

	C++:

	```cpp
	int main(int argc, char *argv[])
	{
		return 0;
	}
	```

	Python:

	```python
	def main():
		print('Hello')

	if __name__ == '__main__':
		main()
	```

Then compile the example (`--listings` is needed only for this example):

```
pandoc input.md --filter pandoc-code-attribute --listings -o output.pdf
```


### Command

In general, to use this filter, just add this filter to pandoc command:

```
pandoc input.md --filter pandoc-code-attribute -o output.pdf
```



## License

MIT License

