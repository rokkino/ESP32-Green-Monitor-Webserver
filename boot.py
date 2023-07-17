from MicroWebSrv2  import *
from time          import sleep
import network
import machine
import json
import gc

# ============================================================================
waterpump14 = machine.Pin(14, machine.Pin.OUT)
humidity15 = machine.Pin(15, machine.Pin.OUT)
led16 = machine.Pin(16, machine.Pin.OUT)  # Assuming the LED is connected to GPIO pin 16
# ============================================================================

# Check initial free heap size
#initial_free_heap = gc.mem_free()
#print("Initial free heap:", initial_free_heap)


config_file = "wifi_config.json"

# Load stored Wi-Fi configuration
def load_wifi_config():
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# Save Wi-Fi configuration
def save_wifi_config(ssid, password):
    config = {"ssid": ssid, "password": password}
    with open(config_file, "w") as f:
        json.dump(config, f)


# Connect to Wi-Fi using stored or provided credentials
def connect_to_wifi():
  


    wifi_config = load_wifi_config()
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        if wifi_config:
            ssid = wifi_config.get('ssid')
            password = wifi_config.get('password')
            print('Connecting to network using stored credentials...')
            sta_if.active(True)

            sta_if.connect(ssid, password)
            for _ in range(10):  # Wait for up to 10 seconds for a connection
                if sta_if.isconnected():
                    break
                sleep(3)
        else:
            print('No stored Wi-Fi configuration found.')

    if sta_if.isconnected():
        print('Connected to Wi-Fi. Network config:', sta_if.ifconfig())




    else:
        print('No connection to stored Wi-Fi. Starting Green Monitor access point mode...')
        sta_if.active(False)  # Disable station mode
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(True)



        ap_if.config(essid='Green Monitor', authmode=network.AUTH_OPEN)
        print('Green Monitor access point mode started. Network config:', ap_if.ifconfig())




# Call the connect_to_wifi function to connect on startup
connect_to_wifi()


# ============================================================================ 

@WebRoute(GET, '/waterpumpon')
def _httpHandlerLedOnGet(microWebSrv2, request):
    waterpump14.on()
    request.Response.SetStatus(200)
    request.Response.ReturnOk()
    return True

@WebRoute(GET, '/waterpumpoff')
def _httpHandlerLedOffGet(microWebSrv2, request):
    waterpump14.off()
    request.Response.ReturnOk()
    return True
    
@WebRoute(GET, '/humidity15_On')
def _httpHandlerLedOnGet(microWebSrv2, request):
    humidity15.on()
    request.Response.SetStatus(200)
    request.Response.ReturnOk()
    return True

@WebRoute(GET, '/humidity15_Off')
def _httpHandlerLedOffGet(microWebSrv2, request):
    humidity15.off()
    request.Response.ReturnOk()
    return True
    
@WebRoute(GET, '/ledon')
def _httpHandlerLedOnGet(microWebSrv2, request):
    led16.on()
    request.Response.SetStatus(200)
    request.Response.ReturnOk()
    return True

@WebRoute(GET, '/ledoff')
def _httpHandlerLedOffGet(microWebSrv2, request):
    led16.off()
    request.Response.ReturnOk()
    return True    

@WebRoute(GET, '/checkdevice')
def _httpHandlerCheckLED(microWebSrv2, request):
    statusled16 = led16.value()  # Assuming led16 is the Pin object representing Pin16
    statushumidity15 = humidity15.value()  # Assuming humidity15 is the Pin object representing Pin15
    statuswaterpump14 = waterpump14.value()  # Assuming waterpump14 is the Pin object representing Pin14

    response = {
        'statusled16': statusled16,
        'statushumidity15': statushumidity15,
        'statuswaterpump14': statuswaterpump14,
    }
    request.Response.ReturnJSON(200, response)
    return True

@WebRoute(GET, '/wifiscan')
def wifi_scan_handler(microWebSrv2, request):
    import network
    import json
    # Connect to Wi-Fi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    # Scan for Wi-Fi networks
    scan_results = wifi.scan()

    # Prepare a list to store network information
    network_list = []

    # Process and store network information
    for ssid, bssid, channel, rssi, authmode, hidden in scan_results:
        ssid_str = ssid.decode('utf-8')  # Convert bytes to string
        network_info = {
            'ssid': ssid_str,
            'channel': channel,
            'power': rssi,
            'auth_mode': authmode
        }
        network_list.append(network_info)  # Append each network_info object to the array
    	
    request.Response.ReturnJSON(200, network_list)


@WebRoute(GET, '/devicetimerget')
def _httpHandlerCheckDevice(microWebSrv2, request):
    try:
        # Read the device information from the JSON file
        with open('devicetimer.json', 'r') as file:
            device_info = json.load(file)

        # Send the device information as the response
        request.Response.ReturnJSON(200, device_info)
    except Exception as e:
        # Log the exception (if logging is available)
        print("Exception:", str(e))

        # In case of any error, return a bad request response
        request.Response.ReturnBadRequest()
        


@WebRoute(POST, '/devicetimerpost')
def _httpHandlerAddTimer(microWebSrv2, request):
    try:
        # Parse the JSON data from the request body
        data = request.GetPostedJSONObject()

        # Read the existing timers from the JSON file
        with open('devicetimer.json', 'r') as file:
            timers = json.load(file)

        # Check if timers is a list, otherwise initialize as an empty list
        if not isinstance(timers, list):
            timers = []

        # Add the new timer to the list of timers
        timers.append(data)

        # Write the updated timers back to the JSON file
        with open('devicetimer.json', 'w') as file:
            json.dump(timers, file)

        # Print the array of JSON timers
        print("Timers:", timers)

        # Return a success response
        request.Response.ReturnJSON(200, timers)

    except Exception as e:
        # Log the exception (if logging is available)
        print("Exception:", str(e))

        # In case of any error, return a bad request response
        request.Response.ReturnBadRequest()


@WebRoute(POST, '/connect')
def connect_handler_post(microWebSrv2, request):
    # Parse the JSON data from the request body
    try:
        data = request.GetPostedJSONObject()
        ssid = data.get('ssid')
        password = data.get('password')
    except:
        request.Response.ReturnBadRequest()

    # Save the SSID and password to wifi_config file
    wifi_config = {
        'ssid': ssid,
        'password': password
    }
    with open('wifi_config.json', 'w') as file:
        json.dump(wifi_config, file)

    content = json.dumps({'message': 'Connection successful'})

    # Send the response
    request.Response.ReturnOk(content)
	
    # Reboot the MCU
    machine.reset()

# ============================================================================
MicroWebSrv2.AddDefaultPage('overview.html')


# ------------------------------------------------------------------------


# Instanciates the MicroWebSrv2 class,
mws2 = MicroWebSrv2()


# SSL is not correctly supported on MicroPython.
# But you can uncomment the following for standard Python.
#mws2.EnableSSL( certFile = 'SSL-Cert/openhc2.crt',
 #               keyFile  = 'SSL-Cert/openhc2.key' )

# For embedded MicroPython, use a very light configuration,
mws2.SetEmbeddedConfig() # very minimal setting
#mws2.SetLightConfig() #light setting

# All pages not found will be redirected to the home '/',
mws2.NotFoundURL = '/overview.html'
# Starts the server as easily as possible in managed mode,
mws2.StartManaged()


