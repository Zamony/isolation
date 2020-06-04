**isolation** is a two-player strategy board game. It is played on a 7x7 board which is initially filled with squares.

Rules are really simple:
1. Moving one's piece to a neighboring position that contains a square but not the opponent's piece
2. Removing any square with no piece on it

The player who cannot make any move loses the game


![Isolation UI](https://raw.githubusercontent.com/Zamony/zamony.github.io/master/img/isolation_actual.png)

[UI layout draft](https://raw.githubusercontent.com/Zamony/zamony.github.io/master/img/IsolationLayout.png)

## Installation
There are three installation options, which one to prefer depends on your needs:
+ Installation via Python wheel (you can download wheel file from releases page)
```bash
pip install isolation.whl
isolation  # run the game
```
You can always build a wheel yourself (the produced binary will be in `dist` folder)
```bash
git clone https://github.com/Zamony/isolation.git
cd isolation
make wheel
```

+ Installation from source code
```bash
git clone https://github.com/Zamony/isolation.git
cd isolation
make run # run the game
```

It is also possible to run `isolation` without Make utility:
```bash
python -m pip install --user -r requirements.txt # install requirements
python main.py # run the game
```

+ Installation via binary distribution. You can download Linux binary from releases page.
You can always build a binary yourself (the produced binary will be in `dist` folder)
```bash
git clone https://github.com/Zamony/isolation.git
cd isolation
make build
```

## Features
+ GUI interface
+ Support for Windows and Linux
+ Russian/English versions of the game
+ Multiple difficulty levels
+ Playing over the Internet
+ Text mode

## Developer notes
There are some additional targets in the Makefile
+ Check projects for warnings and errors: `make lint`
+ Generate documentation in doc directory: `make doc`
+ Run unit tests: `make run-unit-tests`
+ Run functional tests: `make run-func-tests`
+ Clean generated files: `make clean`
