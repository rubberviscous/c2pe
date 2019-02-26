# c2pe

This command line interface enables translation of Chinese characters to english and pinyin in nicely formatted text output.

input
```bash
手中握着格桑花呀
```

output
```bash
手中握着格桑花呀
shǒuzhōngwòzháogésānghuāyā
Holding Gesang flowers in my hand
```
## Installation

This CLI requires Python 3 and above.
```bash
pip install c2pe
```

## Usage

```bash
c2pe <path to file>
```
By default, if no `--output` is provided, the translation will be directed to stdout.

To save to file:

```bash
c2pe ~/my_file.txt --output ~/my_file_translated.txt
```
## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D