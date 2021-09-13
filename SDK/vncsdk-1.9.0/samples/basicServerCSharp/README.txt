# Building and running the basicServer C# sample app for Windows

This single-shot sample Server app remotes the desktop of the currently 
logged-in user only. It cannot remote the login, lock, and User Account 
Control screens, nor inject Ctrl+Alt+Delete on Windows Vista+ computers. 
Screen capture does not persist between log and switch outs. For a 
persistent sample app demonstrating this behavior, see 
<vnc-sdk>\samples\serviceServerWin.


## Requirements

* Visual Studio 2017 or 2015 (for C# 6) allows you to build the project as-is,
  targeting .NET framework 4.6.1 by default.
* Visual Studio 2010+ is supported but appropriate modifications to the sample
  are required for earlier versions of the C# specification, such as removing
  the auto property initialisers.
* Earlier .NET 4+ framework targets may also require changes to the project and
  sample code.


## Building the sample app

Use the included Project files with Visual Studio:
You can optionally hard-code connectivity information in Program.cs
before compiling. This may be convenient if you are deploying to a single 
device. If you are deploying to multiple devices, instruct device users 
to provide this information at run-time instead. See the final section 
for more information.
 

## Deploying the sample app to other devices

If you want to run this sample app on multiple devices, deploy the following files:
 
* BasicServerCSharp.exe (sample app binary)
* RealVNC.VncSdk.dll (C# binding library)
* vncsdk.dll (SDK library)
* vncsdk.dll (SDK library)
* vncannotator.exe (if annotations are supported)

The sample app binary expects to find the SDK files in the same directory or in the
directory specified in the VNCSDK_LIBRARY environment variable.


## Providing connectivity information and running the sample app

You can either join VNC Cloud and let it manage connectivity for you, or 
establish direct connections (UDP or TCP) computers listening on known 
IP addresses and ports. Or enable the sample app to do both.

### Joining VNC Cloud

You must provide a separate Cloud address for each device you deploy the
sample app to. Use <vnc-sdk>\tools\vnccloudaddresstool to freely obtain
Cloud addresses in conjunction with your sandbox API key, or call the 
VNC Cloud API directly.

If the sample app will run on a single device, optionally hard-code the 
Cloud address and Cloud password in basicServer.cxx before compiling.

To deploy to multiple devices, do not hard-code but instead instruct device
users to provide this information at run-time in the following format:

<configuration>\basicServerCSharp.exe <Cloud-addr> <Cloud-pwd>

### Listening for direct connections (UDP or TCP)

1) Sign in to your RealVNC account and follow the instructions on the 
   Add-on codes page to obtain a trial direct connectivity add-on code.
2) Apply the code in basicServer.cxx and recompile. If the sample app will 
   run on a single device, optionally hard-code a listening port as well 
   (the default for VNC is 5900).
3) If deploying to multiple devices, instruct device users to provide this 
   information at run-time instead:

   <configuration>\basicServerCSharp.exe <ip-port>

Note the sample app will listen on all IPv4 and IPv6 addresses available to 
the device. To deter MITM attacks, inform Viewer app users of the device's 
unique, memorable catchphrase (printed to the console at run-time).

### Joining VNC Cloud *and* listening for direct connections

With the exception of the direct connectivity add-on code (which must always be 
hard-coded in Program.cs), you can instruct device users to 
provide all the connectivity information required at the command line:

<configuration>\basicServerCSharp.exe <Cloud-addr> <Cloud-pwd> <ip-port>
 

Copyright (C) 2016-2020 RealVNC Limited. All rights reserved.
