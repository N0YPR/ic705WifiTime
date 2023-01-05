# ic705WifiTime
This script is for those operating their Icom IC-705 out on a SOTA/POTA activation where they may not have any
connectivity to the internet to accurately set the clock on their computer as required by digital modes such as 
FT8 or JS8-Call.

The IC-705 is very susceptible to RF interference if you connect it to your computer using a USB cable. So many of us
choose to connect to the radio via its built in WiFi using something like https://github.com/nonoo/kappanhang or
https://wfview.org/.

But because the [CI-V](https://www.icomeurope.com/wp-content/uploads/2020/08/IC-705_ENG_CI-V_1_20200721.pdf) protocol 
used to communicate with the radio only returns the time to the nearest minute, this script will run for up to 60 
seconds while it waits to detect the top of a minute.

# Usage
python3 set_time_from_ic705.py <serial_port_name>

note on naming of kappanhang virtual serial ports:

I have my radio's Network Radio Name (Menu->Set->WLAN Set->Remote Settings->Network Radio Name)
set to N0YPR-705 and therefore the virtual serial port that kappanhang creates for me is /tmp/kappanhang-N0YPR-705.pty

# TODO
* properly package/setup things
