import sys
import os
from pathlib import Path, PurePath
from subprocess import Popen
import yaml
import pyxml
import random

argument_error = "Chybný počet argumentů.\nPoužití: "
project = None
msbuild = None
root_attribs = [
    {"x:Class":      "{0}.MainWindow"},
    {"xmlns":        "http://schemas.microsoft.com/winfx/2006/xaml/presentation"},
    {"xmlns:x":      "http://schemas.microsoft.com/winfx/2006/xaml"},
    {"xmlns:d":      "http://schemas.microsoft.com/expression/blend/2008"},
    {"xmlns:mc":     "http://schemas.openxmlformats.org/markup-compatibility/2006"},
    {"xmlns:local":  "clr-namespace:{0}"},
    {"mc:Ignorable": "d"}
]

def new_project(*args):
    if not os.path.exists(args[0]):
        os.mkdir(args[0])
    for i in os.listdir("template"):
        if os.path.isdir("template/" + i):
            continue
        with open(os.path.join("template", i)) as f:
            contents = "".join([x.format(*args) for x in f.readlines()])
        with open(os.path.join(args[0], i), "w") as f:
            f.write(contents)
    project = args[0]
    os.chdir(project)
    
def yaml_to_xml(data, toplevel=True):
    elements = []
    for i, j in data.items():
        if i[-4:].isnumeric():
            i = i[:-4]
        elem = pyxml.Element(i)
        if isinstance(j, dict):
            for k in yaml_to_xml(j, False):
                elem.append(k)
        elif isinstance(j, list):
            for k in j:
                key = list(k)[0]
                if isinstance(k[key], dict):
                    for l in yaml_to_xml(k, False):
                        elem.append(l)
                else:
                    elem.attrib[key] = k[key]
        elements.append(elem)

    if toplevel:
        elements = elements[0]
    return elements
    
def build_project():
    for i in [x for x in os.listdir() if x.endswith("yaml")]:
        with open(i) as f:
            file_contents = f.read()
        file_contents = file_contents.split("\n")
        for j in range(len(file_contents)):
            if file_contents[j].endswith(":") and file_contents[j] != "Window:":
                file_contents[j] = file_contents[j][:-1] + str(random.randint(1000, 9999)) + ":"
        file_contents = "\n".join(file_contents)
        print(file_contents)
        yaml_data = yaml.safe_load(file_contents)
        for k in range(len(root_attribs)):
            key = list(root_attribs[k].keys())[0]
            root_attribs[k][key] = root_attribs[k][key].format(PurePath(os.getcwd()).parts[-1])
        yaml_data["Window"] = root_attribs + yaml_data["Window"]
        xaml_data = yaml_to_xml(yaml_data)

        with open(i.replace(".yaml", ".xaml"), "wb") as f:
            pyxml.ElementTree.write(pyxml.ElementTree(xaml_data), f, encoding="utf-8")
        with open(i.replace(".yaml", ".xaml"), "r+") as f:
            data = f.read()
            f.seek(0)
            f.truncate()
            f.write(data.replace("&nbsp;", " "))

        try:
            Popen(("dotnet", "build"))
        except FileNotFoundError:
            try:
                Popen((os.environ["DOTNET_HOME"], "dotnet", "build"))
            except KeyError:
                sys.exit("Příkaz 'dotnet' nenalezen. Nastav proměnnou prostředí DOTNET_HOME a zkus to znovu.")

def run(command):
    if command[0] == "new":
        if len(command) < 3:
            print(argument_error + "wpftools new <název projektu> <verze .NET>")
            print("Verze .NET může být: v4.7.2 net8.0-windows nebo jiná verze .NET.")
            return
        new_project(*command[1:])
    elif command[0] == "build":
        if len(command) > 1:
            print(argument_error + "wpftools build")
            return
        build_project()

if __name__ == "__main__":   
    if len(sys.argv) == 1:
        while True:
            try:
                command = input("wpf_yaml> ")
                if command == "exit":
                    break
                run(command.split(" "))
            except EOFError:
                break
    else:
        run(sys.argv[1:])
