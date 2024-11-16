for this tool to run  you would need pyqt5 and  libimobiledevice download both and run the .py file PyQt5 - Comprehensive Python Bindings for Qt v5
Qt is set of cross-platform C++ libraries that implement high-level APIs for accessing many aspects of modern desktop and mobile systems. These include location and positioning services, multimedia, NFC and Bluetooth connectivity, a Chromium based web browser, as well as traditional UI development.

PyQt5 is a comprehensive set of Python bindings for Qt v5. It is implemented as more than 35 extension modules and enables Python to be used as an alternative application development language to C++ on all supported platforms including iOS and Android.

PyQt5 may also be embedded in C++ based applications to allow users of those applications to configure or enhance the functionality of those applications.

Author
PyQt5 is copyright (c) Riverbank Computing Limited. Its homepage is https://www.riverbankcomputing.com/software/pyqt/.

Support may be obtained from the PyQt mailing list at https://www.riverbankcomputing.com/mailman/listinfo/pyqt/.

License
PyQt5 is released under the GPL v3 license and under a commercial license that allows for the development of proprietary applications.

Documentation
The documentation for the latest release can be found here.

Installation
The GPL version of PyQt5 can be installed from PyPI:

pip install PyQt5
pip will also build and install the bindings from the sdist package but Qt's qmake tool must be on PATH.

The sip-install tool will also install the bindings from the sdist package but will allow you to configure many aspects of the installation.

 # libimobiledevice

*A library to communicate with services on iOS devices using native protocols.*

![](https://github.com/libimobiledevice/libimobiledevice/actions/workflows/build.yml/badge.svg)

## Features

libimobiledevice is a cross-platform software library that talks the protocols
to interact with iOS devices.

Unlike other projects, it does not depend on using any existing proprietary
libraries and does not require jailbreaking.

Some key features are:

- **Interface**: Implements many high-level interfaces for device services
- **Implementation**: Object oriented architecture and service abstraction layer
- **Cross-Platform:** Tested on Linux, macOS, Windows and Android platforms
- **Utilities**: Provides various command-line utilities for device services
- **SSL**: Allows choosing between OpenSSL, GnuTLS, or MbedTLS to handle SSL communication
- **Network**: Supports network connections with "WiFi sync" enabled devices
- **Python:** Provides Cython based bindings for Python

The implemented interfaces of many device service protocols allow applications
to:

* Access filesystem of a device
* Access documents of file sharing apps
* Retrieve information about a device and modify various settings
* Backup and restore the device in a native way compatible with iTunes
* Manage app icons arrangement on the device
* Install, remove, list and basically manage apps
* Activate a device using official servers
* Manage contacts, calendars, notes and bookmarks
* Retrieve and remove crashreports
* Retrieve various diagnostics information
* Establish a debug connection for app debugging
* Mount filesystem images
* Forward device notifications
* Manage device provisioning
* Take screenshots from the device screen (requires mounted developer image)
* Simulate changed geolocation of the device (requires mounted developer image)
* Relay the syslog of the device
* Expose a connection for WebKit remote debugging

... and much more.

The library is in development since August 2007 with the goal to bring support
for these devices to the Linux Desktop.

## Installation / Getting started

### Debian / Ubuntu Linux

First install all required dependencies and build tools:
```shell
sudo apt-get install \
	build-essential \
	pkg-config \
	checkinstall \
	git \
	autoconf \
	automake \
	libtool-bin \
	libplist-dev \
	libusbmuxd-dev \
	libimobiledevice-glue-dev \
	libtatsu-dev \
	libssl-dev \
	usbmuxd
```
NOTE: [libtatsu](https://github.com/libimobiledevice/libtatsu) (and thus `libtatsu-dev`)
is a new library that was just published recently, you have to
[build it from source](https://github.com/libimobiledevice/libtatsu?tab=readme-ov-file#building).

If you want to optionally build the documentation or Python bindings use:
```shell
sudo apt-get install \
	doxygen \
	cython
```

Then clone the actual project repository:
```shell
git clone https://github.com/libimobiledevice/libimobiledevice.git
cd libimobiledevice
```

Now you can build and install it:
```shell
./autogen.sh
make
sudo make install
```

If you require a custom prefix or other option being passed to `./configure`
you can pass them directly to `./autogen.sh` like this:
```bash
./autogen.sh --prefix=/opt/local --enable-debug
make
sudo make install
```

By default, OpenSSL will be used as TLS/SSL library. If you prefer GnuTLS,
configure with `--with-gnutls` like this:
```bash
./autogen.sh --with-gnutls
```

MbedTLS is also supported and can be enabled by passing `--with-mbedtls` to
configure. If mbedTLS is not installed in a default location, you need to set
the environment variables `mbedtls_INCLUDES` to the path that contains the
MbedTLS headers and `mbedtls_LIBDIR` to set the library path. Optionally,
`mbedtls_LIBS` can be used to set the library names directly. Example:
```bash
./autogen.sh --with-mbedtls mbedtls_INCLUDES=/opt/local/include mbedtls_LIBDIR=/opt/local/lib
```

## Usage

Documentation about using the library in your application is not available yet.
The "hacker way" for now is to look at the implementation of the included
utilities.

### Utilities

The library bundles the following command-line utilities in the tools directory:

| Utility                    | Description                                                        |
| -------------------------- | ------------------------------------------------------------------ |
| `idevice_id`               | List attached devices or print device name of given device         |
| `idevicebackup`            | Create or restore backup for devices (legacy)                      |
| `idevicebackup2`           | Create or restore backups for devices running iOS 4 or later       |
| `idevicebtlogger`          | Capture Bluetooth HCI traffic from a device (requires log profile) |
| `idevicecrashreport`       | Retrieve crash reports from a device                               |
| `idevicedate`              | Display the current date or set it on a device                     |
| `idevicedebug`             | Interact with the debugserver service of a device                  |
| `idevicedebugserverproxy`  | Proxy a debugserver connection from a device for remote debugging  |
| `idevicediagnostics`       | Interact with the diagnostics interface of a device                |
| `ideviceenterrecovery`     | Make a device enter recovery mode                                  |
| `ideviceimagemounter`      | Mount disk images on the device                                    |
| `ideviceinfo`              | Show information about a connected device                          |
| `idevicename`              | Display or set the device name                                     |
| `idevicenotificationproxy` | Post or observe notifications on a device                          |
| `idevicepair`              | Manage host pairings with devices and usbmuxd                      |
| `ideviceprovision`         | Manage provisioning profiles on a device                           |
| `idevicescreenshot`        | Gets a screenshot from the connected device                        |
| `idevicesetlocation`       | Simulate location on device                                        |
| `idevicesyslog`            | Relay syslog of a connected device                                 |
| `afcclient`                | Interact with device filesystem via AFC/HouseArrest                |

Please consult the usage information or manual pages of each utility for a
documentation of available command line options and usage examples like this:
```shell
ideviceinfo --help
man ideviceinfo
```

## Contributing

We welcome contributions from anyone and are grateful for every pull request!

If you'd like to contribute, please fork the `master` branch, change, commit and
send a pull request for review. Once approved it can be merged into the main
code base.

If you plan to contribute larger changes or a major refactoring, please create a
ticket first to discuss the idea upfront to ensure less effort for everyone.

Please make sure your contribution adheres to:
* Try to follow the code style of the project
* Commit messages should describe the change well without being too short
* Try to split larger changes into individual commits of a common domain
* Use your real name and a valid email address for your commits

We are still working on the guidelines so bear with us!

## Links

* Homepage: https://libimobiledevice.org/
* Repository: https://github.com/libimobiledevice/libimobiledevice.git
* Repository (Mirror): https://git.libimobiledevice.org/libimobiledevice.git
* Issue Tracker: https://github.com/libimobiledevice/libimobiledevice/issues
* Mailing List: https://lists.libimobiledevice.org/mailman/listinfo/libimobiledevice-devel
* Twitter: https://twitter.com/libimobiledev

## License

This library and utilities are licensed under the [GNU Lesser General Public License v2.1](https://www.gnu.org/licenses/lgpl-2.1.en.html),
also included in the repository in the `COPYING` file.

## Credits

Apple, iPhone, iPad, iPod, iPod Touch, Apple TV, Apple Watch, Mac, iOS,
iPadOS, tvOS, watchOS, and macOS are trademarks of Apple Inc.

This project is an independent software and has not been authorized, sponsored,
or otherwise approved by Apple Inc.

README Updated on: 2024-10-22
