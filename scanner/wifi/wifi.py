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
        self.filter_mac_addresses = True  # Filter MAC addresses against the OUI list
        self.include_random_mac_addresses = True  # Include common random OUI addresses
        self.nearby = True  # Limit to devices that are nearby (rssi > -70)
        self.print_json = False  # Print smartphone data

    def discover_devices(self, scan_time_in_sec):
        """Scans for nearby WiFi devices"""
        # print("Using %s adapter and scanning for %s seconds..." %
        #       (self.adapter, scan_time_in_sec))

        dump_file = "/tmp/tshark-temp"

        # Scan with tshark
        command = [self.tshark, "-I", "-i", self.adapter, "-a",
                   "duration:" + str(scan_time_in_sec), "-w", dump_file]
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
        run_tshark = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, nothing = run_tshark.communicate()

        found_mac_addresses = {}
        for line in output.decode("utf-8").split("\n"):
            if line.strip() == "":
                continue
            mac = line.split()[0].strip().split(",")[0]
            dats = line.split()
            if len(dats) == 3:
                if ":" not in dats[0] or len(dats) != 3:
                    continue
                if mac not in found_mac_addresses:
                    found_mac_addresses[mac] = []
                dats_2_split = dats[2].split(",")
                if len(dats_2_split) > 1:
                    rssi = float(dats_2_split[0]) / \
                        2 + float(dats_2_split[1]) / 2
                else:
                    rssi = float(dats_2_split[0])
                found_mac_addresses[mac].append(rssi)

        if not found_mac_addresses:
            print("Found no signals. Make sure %s supports monitor mode." %
                  self.adapter)
            no_devices_found = 0
            return no_devices_found

        for key, value in found_mac_addresses.items():
            found_mac_addresses[key] = float(sum(value)) / float(len(value))

        known_manufacturers = self.get_known_manufacturers()
        known_random_mac_addresses = self.get_known_random_mac_addresses()
        smartphone_data = []

        for mac in found_mac_addresses:
            company_name = "Not in OUI"
            mac_oui = mac[:8]
            if mac_oui in self.oui_list:
                company_name = self.oui_list[mac_oui]

            if self.include_random_mac_addresses:
                if mac_oui in known_random_mac_addresses:
                    smartphone_data.append(
                        {"company": "randomizationDetected", "rssi": found_mac_addresses[mac], "mac": mac})
                    continue

            if not self.filter_mac_addresses or company_name in known_manufacturers:
                rssi_limit = -70
                if not self.nearby or (self.nearby and found_mac_addresses[mac] > rssi_limit):
                    smartphone_data.append(
                        {"company": company_name, "rssi": found_mac_addresses[mac], "mac": mac})

        if self.print_json:
            print(json.dumps(smartphone_data, indent=2))

        people_count = int(len(smartphone_data))
        os.remove(dump_file)
        return people_count

    def get_known_manufacturers(self):
        """Returns a list of known smartphone manufacturers"""
        known_manufacturers = [
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
        return known_manufacturers

    def get_known_random_mac_addresses(self):
        """Returns a list of known random MAC addresses prefixes"""
        known_random_mac_addresses = ["da:a1:19", "92:68:c3"]
        return known_random_mac_addresses

    def load_oui(self):
        """Loads a list of known smartphone manufacturers"""
        oui_dic = "oui.txt"
        if (not os.path.isfile(oui_dic)) or (not os.access(oui_dic, os.R_OK)):
            download_oui(oui_dic)

        oui = load_dictionary(oui_dic)

        if not oui:
            print("couldn\"t load [%s]" % oui_dic)
            sys.exit(1)
        self.oui_list = oui

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
