# README

The Python script `convert.py` can be used to convert infrared serial interface commands (in hexadecimal representation) into a Flipper Zero[^1] compatible infrared[^2] `.ir` file.

Use case: It can be used to convert LEGO MINDSTORMS RCX[^3] (the "yellow programmable brick") infrared commands[^4] (see `LEGO_RCX.json` input file).

The script supports sending multiple multibyte messages at once and adds wait times for message replies by default.


[^1] [Flipper Zero — Portable Multi-tool Device for Geeks](https://flipperzero.one/)

[^2] [Flipper Zero Blog — Taking over TVs with Flipper Zero Infrared Port](https://blog.flipperzero.one/infrared/)

[^3] *Disclaimer: LEGO and MINDSTORMS are trademarks and copyrights of the LEGO Group of companies which does not sponsor, authorize or endorse this site.*

[^4] [RCX 2.0 Firmware Command Overview / LASM bytecode specification](https://www.inf.ed.ac.uk/teaching/courses/sdp/lego/LASM_Bytecodes.pdf)

## Dependencies

A Python 3 environment is required.

The script only imports `sys` and `json` and therefore shouldn't require any additional packages.


## Usage

Run converter and print output on stdout:

```
$ python convert.py LEGO_RCX.json
```

Run converter and pipe output to IR output file:

```
$ python convert.py LEGO_RCX.json > LEGO_RCX.ir
```

Run converter and pipe output to both an IR output file and stdout:

```
$ python convert.py LEGO_RCX.json | tee LEGO_RCX.ir
```

For the format of the `.json` file, inspect `LEGO_RCX.json` example.
