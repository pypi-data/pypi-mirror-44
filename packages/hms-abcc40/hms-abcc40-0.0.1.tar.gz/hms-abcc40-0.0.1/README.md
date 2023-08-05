# Anybus CompactCom 40 REST interface 

Interface for accessing Anybus CompactCom 40 modules via REST

## Installation

To install this package, simply use `pip`

```sh
pip install hms-abcc40
```

## Usage

To print the module name

```python
import hms.abcc40

my_module = hms.abcc40.CompactCom40("1.2.3.4")
print(my_module.module_name)
```

## License

[Apache License 2.0](LICENSE)