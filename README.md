# ic705WifiTime
ic705WifiTime is a script that allows you to set your computer's system datetime from the Icom IC-705 while connected only via Wifi, not USB.

It requires you to be running http://nonoo/kappanhang with the -s option

Because the CI-V protocal used to communicate with the Icom IC-705 only returns the time to the nearest minute, this script will run for up to 60 seconds while it waits to detect the top of a minute.

# Usage
python3 ic705wifitime.py <hostname>

# TODO
* Refactor/improve code
* properly package things
* write better docs
