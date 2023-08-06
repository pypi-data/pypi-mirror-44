# energy_tools

Modest collection of electrical energy calculation tools.

**Content:**

- [Installation](#installation)
    - [Requirements](#requirements)
    - [Installing energy_tools](#installing-energy_tools)
        - [With pip](#with-pip)
        - [Without pip](#without-pip)
        - [Development version](#development-version)
    - [Test your installation](#test-your-installation)
- [Features](#features)
    - [complex](#complex)
    - [energy_factors](#energy_factors)
    - [misc](#misc)
    - [per_unit](#per_unit)
    - [phasor](#phasor)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation

### Requirements

Basic requirements:

- [Python 3.6+](http://www.python.org/download/releases/);
- numpy.

Development requirements:

- pre-commit;
- pytest;
- twine.

### Installing energy_tools

#### With pip

1. Open a command prompt (e.g. Start > cmd on windows systems);
2. Install energy_tools by running:

```
pip install energy_tools
```

#### Without pip

If you don’t have internet access on your system or don’t want to use pip for some other reason, energy_tools can also be installed without using pip:

1. Download and unzip the current energy_tools distribution from PyPi under “Download files”.
2. Open a command prompt (e.g. Start > cmd on Windows) and navigate to the folder that contains the setup.py file with the command cd <folder> :

```
cd %path_to_energy_tools%\energy_tools-x.x.x\
```

Install energy_tools by running :

```
python setup.py install
```

#### Development version

To install the latest development version of energy_tools from GitLab, simply follow these steps:

1. Download and install git.
2. Open a git shell and navigate to the directory where you want to keep your energy_tools files.
3. Run the following commands:

```
/c/Python36/python.exe -m venv energy_tools
cd energy_tools
git clone https://gitlab.com/miek770/energy_tools.git
source Scripts/activate
python -m pip install -U pip
pip install numpy pre-commit pytest twine
```

4. Navigate inside the repository and check out the develop branch:

```
cd energy_tools
git checkout develop
```

5. Install [Black](https://github.com/ambv/black#version-control-integration) using pre-commit:

```
pre-commit install
```

5. Set your Python path to the outer energy_tools folder (/energy_tools, NOT energy_tools/energy_tools).
6. If necessary, install missing dependencies via pip install (see Development requirements above).

### Test your installation

To test your installed development version, run pytest from the energy_tools' base directory:

```
pytest
```

## Features

`energy_tools` currently includes the following modules:

### complex

The `complex` module includes an improved `EleComplex` class which adds the following attributes (properties): `phase`, `module`.

- `EleComplex.phase` returns the complex number's phase in degrees.
- `EleComplex.module` returns the complex number's amplitude.

The `complex` module also includes a `complex_impedance` function that returns an improved `EleComplex` number, based on a provided real impedance *z* and an *X/R* ratio.

The `EleComplex` class must be imported in order for some of the other tools to be usable:

``` python
from energy_tools.complex import EleComplex
```

See [Usage](#usage) below for more details.

### energy_factors

The `energy_factors` module includes functions to calculate yearly energy factors for special calculations. Currently, it includes the `utilisation_factor` and `loss_factor` functions.

### misc

The `misc` module includes basic functions to manipulate impedances, including `serie`, `parallel`, `zCap` and `zInd`. These calculate series impedance, parallel impedances, capacitance impedance and inductance impedance respectively.

### per_unit

The `per_unit` module includes functions that return the base current, impedance and power.

### phasor

The `phasor` module includes a new data type `Phasor` for the electrical phasor used in power systems.

A phasor is defined by an amplitude and a phase. The instance can be created either using those, or by providing a complex amplitude (in this case the phase is ignored). Several operations are supported, including: addition, substraction, multiplication, division, power, inversion and equality with either another phasor, a float or an integer.

It also provides a nice representation in this form: 120.000 @ 0.000°

Attributes:

- amp: The unitless phasor amplitude.
- pha: The phasor's phase in degrees.
- real: The phasor's real part (interpreted as a complex number).
- imag: The phasor's imaginary part (interpreted as a complex number).

The `phasor` module also includes functions `sequences` and `phasors`. The former retuns phase A's sequence voltages from phase A, B and C's voltages. The latter does the opposite, i.e. it returns phase A, B and C's voltages from phases A's sequence voltages.

## Usage

Sample usage may be found in the [tests](https://gitlab.com/miek770/energy_tools/tree/master/energy_tools/tests) directory. Most of these tools are straightforward (or aim to be), so the tests and docstrings should be helpful enough.

As mentioned [above](#complex), the `EleComplex` class must be imported in order for many of the other tools to be usable:

``` python
from energy_tools.complex import EleComplex
```

When the improved `EleComplex` type is imported this way, the following call will result in variable `a` being an `energy_tools.complex.EleComplex` instance, as expected:

```
a = EleComplex(1, 1)
a.phase #  Will return 45 degrees
```

Implicitly declaring a complex number, however, will return the built-in `complex` type:

```
a = 1 + 1j
a.phase #  Will raise AttributeError
```

## Contributing

If you wish to contribute, please follow the development version instructions above and refer to the project's [contribution guide](https://gitlab.com/miek770/energy_tools/blob/master/CONTRIBUTING.md).
