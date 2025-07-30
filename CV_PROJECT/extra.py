import subprocess

def get_ram_info():
    command = 'powershell "Get-CimInstance Win32_PhysicalMemory | Select-Object Manufacturer, Speed, MemoryType, SMBIOSMemoryType"'
    output = subprocess.check_output(command, shell=True).decode()
    print(output)

get_ram_info()
