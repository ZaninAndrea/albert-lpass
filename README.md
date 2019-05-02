# Albert LastPass integration

This extension add LastPass integration to [Albert](https://github.com/albertlauncher/albert). You can search and copy any password in your LastPass account using the prefix `lp`.

## Installing

To install run this script:

```bash
pip install fuzzywuzzy # fuzzy matching python library
wget https://raw.githubusercontent.com/ZaninAndrea/albert-lpass/master/lpass.py -O /usr/share/albert/org.albert.extension.python/modules
```

The follow the [official instructions](https://github.com/lastpass/lastpass-cli) to install the `lpass` cli tool, finally activate the LastPass integration from Albert settings under Extensions -> Python -> LastPass
