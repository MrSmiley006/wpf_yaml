# wpf_yaml
Překladač návrhů GUI napsaných v YAMLu do XAMLu pro WPF a s ním více či méně kompatibilní knihovny.

Pokyny k sestavení
------------------
1. Naklonujte tento repozitář: `git clone https://github.com/MrSmiley006/wpf_yaml.git`
2. Přejděte do adresáře s programem: `cd wpf_yaml`
3. Přeložte program tímto příkazem: `pyinstaller wpf_yaml.py --onefile --add-data template:template`
   nebo
3. Spusťe program přímo ze zdrojového kódu: `python wpf_yaml.py [příkaz] [parametry]`

---
A YAML to XAML transpiler for designing GUIs in WPF and more or less compatible GUI libraries.

Building instructions
---------------------
1. Clone this repository: `git clone https://github.com/MrSmiley006/wpf_yaml.git`
2. Change into the directory: `cd wpf_yaml`
3. Compile the program with this command: `pyinstaller wpf_yaml.py --onefile --add-data template:template`
   or
3. Run the program directly from source code: `python wpf_yaml.py [command] [args]`
