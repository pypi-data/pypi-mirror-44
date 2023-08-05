# pandoc-code-attribute

Pandoc filter to add attributes to code blocks based on their classes.


## Installation

First install python and python-pip.

Then use pip to install:

```
pip3 install --user pandoc-code-attribute
```


## Usage

### Configuration

By default, this filter won't add style attributes to prevent undefined errors.

You can enable it by setting `code-attribute` field in metadata.

To add attributes to all classes, use:

```
code-attribute: true
```

To add attributes to specific classes, use:

```
code-attribute:
	- cpp
```

### Example

This pandoc filter will add attributes to code blocks based on their classes.

For example, it can be very useful to use different styles for different language in `listings` :

	---
	code-attribute:
		- cpp
		- python
	header-includes: |
		\usepackage{listings}
		\usepackage[usenames,dvipsnames]{color}
		
		\lstset{ % General settings
			numbers=left,
			numberstyle=\tiny
		}

		\lstdefinestyle{cpp}{ % Only for C++
			keywordstyle=\color{Green}
		}

		\lstdefinestyle{python}{ % Only for Python
			keywordstyle=\color{Magenta}
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

Results:

<img src="result.png" width="50%" height="50%" />


### Command

In general, to use this filter, just add this filter to pandoc command:

```
pandoc input.md --filter pandoc-code-attribute -o output.pdf
```



## License

MIT License

