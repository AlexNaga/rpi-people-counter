import json
import os
import os.path
import subprocess
import sys
from wifi.oui import load_dictionary, download_oui


class Wifi:
    def __init__(self, adapter):
        self.load_oui()
        self.load_tshark()
        self.adapter = adapter
        self.filter_mac_addresses = True  # Filter MAC addresses against the OUI dictionary
        self.print_json = False  # Print smartphone data
        self.nearby = False  # Limit to devices that are nearby (rssi > -70)
        self.verbose = False

    def discover_devices(self, scantime):
        """Scans for nearby WiFi devices"""
        print("Using %s adapter and scanning for %s seconds..." %
              (self.adapter, scantime))

        dump_file = "/tmp/tshark-temp"

        # Scan with tshark
        command = [self.tshark, "-I", "-i", self.adapter, "-a",
                   "duration:" + str(scantime), "-w", dump_file]
        if self.verbose:
            print(" ".join(command))
        run_tshark = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, nothing = run_tshark.communicate()

        # Read tshark output
        command = [
            self.tshark, "-r",
            dump_file, "-T",
            "fields", "-e",
            "wlan.sa", "-e",
            "wlan.bssid", "-e",
            "radiotap.dbm_antsignal"
        ]
        if self.verbose:
            print(" ".join(command))
        run_tshark = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, nothing = run_tshark.communicate()

        found_macs = {}
        for line in output.decode("utf-8").split("\n"):
            if self.verbose:
                print(line)
            if line.strip() == "":
                continue
            mac = line.split()[0].strip().split(",")[0]
            dats = line.split()
            if len(dats) == 3:
                if ":" not in dats[0] or len(dats) != 3:
                    continue
                if mac not in found_macs:
                    found_macs[mac] = []
                dats_2_split = dats[2].split(",")
                if len(dats_2_split) > 1:
                    rssi = float(dats_2_split[0]) / \
                        2 + float(dats_2_split[1]) / 2
                else:
                    rssi = float(dats_2_split[0])
                found_macs[mac].append(rssi)

        if not found_macs:
            print("Found no signals. Make sure %s supports monitor mode." %
                  self.adapter)
            no_devices_found = 0
            return no_devices_found

        for key, value in found_macs.items():
            found_macs[key] = float(sum(value)) / float(len(value))

        known_smartphones = self.get_known_smartphones()
        smartphone_people = []
        for mac in found_macs:
            oui_id = "Not in OUI"
            if mac[:8] in self.oui_dic:
                oui_id = self.oui_dic[mac[:8]]
            if self.verbose:
                print(mac, oui_id, oui_id in known_smartphones)
            if not self.filter_mac_addresses or oui_id in known_smartphones:
                if not self.nearby or (self.nearby and found_macs[mac] > -70):
                    smartphone_people.append(
                        {"company": oui_id, "rssi": found_macs[mac], "mac": mac})
        if self.verbose:
            print(json.dumps(smartphone_people, indent=2))
        if self.print_json:
            print(json.dumps(smartphone_people, indent=2))

        people_count = int(len(smartphone_people))
        os.remove(dump_file)
        return people_count

    def get_known_smartphones(self):
        """Returns a list of known smartphone manufacturers"""
        known_smartphones = [
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
        return known_smartphones

    def load_oui(self):
        """Loads a list of known smartphone manufacturers"""
        oui_dic = "oui.txt"
        if (not os.path.isfile(oui_dic)) or (not os.access(oui_dic, os.R_OK)):
            download_oui(oui_dic)

        oui = load_dictionary(oui_dic)

        if not oui:
            print("couldn\"t load [%s]" % oui_dic)
            sys.exit(1)
        self.oui_dic = oui

    def load_tshark(self):
        try:
            self.tshark = self.which("tshark")
        except:
            print("tshark not found, install using\n\napt-get install tshark\n")
            sys.exit(1)

    def which(self, program):
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
