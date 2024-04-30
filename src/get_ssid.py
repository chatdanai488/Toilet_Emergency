import subprocess


def get_connected_wifi_ssid():
    try:
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if "SSID" in line:
                ssid = line.split(":")[1].strip()
                return ssid
        return None
    except Exception as e:
        print("Error occurred:", e)
        return None
