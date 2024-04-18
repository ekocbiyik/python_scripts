import psutil
from flask import Flask, jsonify

app = Flask(__name__)

class SystemInfo:
  def __init__(self, cpu_usage, ram_total, ram_used, disk_total, disk_used):
    self.cpu_usage  = f"{cpu_usage:.2f}"
    self.ram_total  = f"{ram_total:.2f}"
    self.ram_used   = f"{ram_used:.2f}"
    self.disk_total = f"{disk_total:.2f}"
    self.disk_used  = f"{disk_used:.2f}"


@app.route('/getUsage', methods=['GET'])
def get_usage():
  cpu_usage = get_cpu_usage()
  ram_total, ram_used = get_ram_usage()
  disk_total, disk_used = get_disk_usage()

  system_info = SystemInfo(cpu_usage, ram_total, ram_used, disk_total, disk_used)
  response = jsonify(system_info.__dict__)
  response.headers['Content-Type'] = 'application/json'
  return response


def get_cpu_usage():
  return psutil.cpu_percent(0.2)


def get_ram_usage():
  ram_total = psutil.virtual_memory().total / (1024 * 1024 * 1024)  # GB
  ram_used = psutil.virtual_memory().used / (1024 * 1024 * 1024)    # GB
  return (ram_total, ram_used)


def get_disk_usage():
  disk_usage = psutil.disk_usage('/')
  disk_total = disk_usage.total / (1024 * 1024 * 1024)  # GB
  disk_used = disk_usage.used / (1024 * 1024 * 1024)    # GB
  return (disk_total, disk_used)


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=45555)


# NOT
# Bu script windows bilgisayarda windows servis olarak çalıştırılmak istenirse "nssm" aracı kullanılabilir.
# dikkat edilmesi gereken kısım ayarlama yapılırken "Logon" sekmesinde ilk kutucuk işaretlenip bilgisayardaki kullanıcı adı ve parola girilmelidir
# aşağıdaki makaleden destek alınabilir.
# https://joe-thomas.medium.com/running-a-python-script-as-a-windows-service-a-guide-a32abbc90172
