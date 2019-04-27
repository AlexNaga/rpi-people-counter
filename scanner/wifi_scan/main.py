import json
import os
import os.path
import subprocess
import sys
import threading
import time

from wifi_scan.oui import load_dictionary, download_oui


def which(program):
    """Determines whether program exists"""
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file


# @click.option("-o", "--out", default=", help="output cellphone data to file")
# @click.option("-d", "--dictionary", default="oui.txt", help="OUI dictionary")
# @click.option("-v", "--verbose", help="verbose mode", is_flag=True)
# @click.option("--number", help="just print the number", is_flag=True)
# @click.option("-j", "--jsonprint", help="print JSON of cellphone data", is_flag=True)
# @click.option("-n", "--nearby", help="only quantify signals that are nearby (rssi > -70)", is_flag=True)
# @click.option("--allmacaddresses", help="do not check MAC addresses against the OUI database to only recognize known cellphone manufacturers", is_flag=True)  # noqa
# @click.option("-m", "--manufacturers", default=", help="read list of known manufacturers from file")
# @click.option("--sort", help="sort cellphone data by distance (rssi)", is_flag=True)
# @click.option("--targetmacs", help="read a file that contains target MAC addresses", default="")
def wifi_scan(adapter, scantime):
    verbose = False
    dictionary = "oui.txt"
    number = False
    nearby = False
    jsonprint = False
    out = False
    allmacaddresses = False
    manufacturers = False
    sort = False
    targetmacs = False

    return scan(adapter, scantime, verbose, dictionary, number,
                nearby, jsonprint, out, allmacaddresses, manufacturers, sort, targetmacs)


def scan(adapter, scantime, verbose, dictionary, number, nearby, jsonprint, out, allmacaddresses, manufacturers, sort, targetmacs):
    """Monitor wifi signals to count the number of people around you"""

    if (not os.path.isfile(dictionary)) or (not os.access(dictionary, os.R_OK)):
        download_oui(dictionary)

    oui = load_dictionary(dictionary)

    if not oui:
        print("couldn\"t load [%s]" % dictionary)
        sys.exit(1)

    try:
        tshark = which("tshark")
    except:
        print("tshark not found, install using\n\napt-get install tshark\n")
        sys.exit(1)

    if jsonprint:
        number = True
    if number:
        verbose = False

    print("Using %s adapter and scanning for %s seconds..." %
          (adapter, scantime))

    dump_file = "/tmp/tshark-temp"

    # Scan with tshark
    command = [tshark, "-I", "-i", adapter, "-a",
               "duration:" + str(scantime), "-w", dump_file]
    if verbose:
        print(" ".join(command))
    run_tshark = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, nothing = run_tshark.communicate()

    # Read tshark output
    command = [
        tshark, "-r",
        dump_file, "-T",
        "fields", "-e",
        "wlan.sa", "-e",
        "wlan.bssid", "-e",
        "radiotap.dbm_antsignal"
    ]
    if verbose:
        print(" ".join(command))
    run_tshark = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, nothing = run_tshark.communicate()

    foundMacs = {}
    for line in output.decode("utf-8").split("\n"):
        if verbose:
            print(line)
        if line.strip() == "":
            continue
        mac = line.split()[0].strip().split(",")[0]
        dats = line.split()
        if len(dats) == 3:
            if ":" not in dats[0] or len(dats) != 3:
                continue
            if mac not in foundMacs:
                foundMacs[mac] = []
            dats_2_split = dats[2].split(",")
            if len(dats_2_split) > 1:
                rssi = float(dats_2_split[0]) / 2 + float(dats_2_split[1]) / 2
            else:
                rssi = float(dats_2_split[0])
            foundMacs[mac].append(rssi)

    if not foundMacs:
        print("Found no signals, are you sure %s supports monitor mode?" % adapter)
        sys.exit(1)

    for key, value in foundMacs.items():
        foundMacs[key] = float(sum(value)) / float(len(value))

    if manufacturers:
        f = open(manufacturers, "r")
        cellphone = [line.rstrip("\n") for line in f.readlines()]
        f.close()
    else:
        cellphone = [
            "Motorola Mobility LLC, a Lenovo Company",
            "GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD",
            "Huawei Symantec Technologies Co.,Ltd.",
            "Microsoft",
            "HTC Corporation",
            "Samsung Electronics Co.,Ltd",
            "SAMSUNG ELECTRO-MECHANICS(THAILAND)",
            "BlackBerry RTS",
            "LG ELECTRONICS INC",
            "Apple, Inc.",
            "LG Electronics",
            "OnePlus Tech (Shenzhen) Ltd",
            "Xiaomi Communications Co Ltd",
            "LG Electronics (Mobile Communications)"]

    cellphone_people = []
    for mac in foundMacs:
        oui_id = "Not in OUI"
        if mac[:8] in oui:
            oui_id = oui[mac[:8]]
        if verbose:
            print(mac, oui_id, oui_id in cellphone)
        if allmacaddresses or oui_id in cellphone:
            if not nearby or (nearby and foundMacs[mac] > -70):
                cellphone_people.append(
                    {"company": oui_id, "rssi": foundMacs[mac], "mac": mac})
    if sort:
        cellphone_people.sort(key=lambda x: x["rssi"], reverse=True)
    if verbose:
        print(json.dumps(cellphone_people, indent=2))

    num_people = int(len(cellphone_people))

    if number and not jsonprint:
        print(num_people)
    elif jsonprint:
        print(json.dumps(cellphone_people, indent=2))

    if out:
        with open(out, "a") as f:
            data_dump = {"cellphones": cellphone_people, "time": time.time()}
            f.write(json.dumps(data_dump) + "\n")
        if verbose:
            print("Wrote %d records to %s" % (len(cellphone_people), out))

    os.remove(dump_file)

    return num_people
