/*
Copyright (C) 2016-2017 RealVNC Limited. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include <iostream>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <vnc/Vnc.h>

#include "BasicViewerWindow.h"

/*
 * basicViewerX11 sample
 *
 * This cross-platform sample shows how to implement a basic VNC viewer using
 * the VNC SDK, running on Linux using X11.
 *
 * Two types of connectivity are supported: Cloud-based and direct connectivity (UDP or TCP).
 * A viewer can only use one of these mechanisms at a time.
 *
 * Note: To use direct connectivity you will need to apply an add-on code; a trial
 * code is available from your RealVNC account. You can ignore direct connectivity related
 * code below if you do not intend to use the direct connectivity add-on.
 *
 * The viewer attempts to connect to a server, using either Cloud-based or
 * direct connectivity, according to user-supplied connectivity details.
 * These details can be provided on the command line or built-in using macro
 * definitions below.
 */

/* For Cloud connections, either hard-code the Cloud address for the Viewer OR
 * specify it at the command line. Example Cloud address:
 * LxygGgSrhXQFiLj5M4M.LxyPXzA9sGLkB6pCtJv.devEX1Sg2Txs1CgVuW4.LxyPRsVnXoDoue4Xqm
 */
#define LOCAL_CLOUD_ADDRESS ""

/* Either hard-code the Cloud password associated with this Cloud address OR
 * specify it at the command line. Example Cloud password: KMDgGgELSvAdvscgGfk2
 */
#define LOCAL_CLOUD_PASSWORD ""

/* Either hard-code the Cloud address of the Server (peer) to connect to OR
 * specify it at the command line. Example peer Cloud address:
 * LxyDgGgrhXQFiLj5M4M.LxyPXzA9sGLkB6pCtJv.devEX1Sg2Txs1CgVuW4.LxyPRydf9ZczNo13BcD
 */
#define PEER_CLOUD_ADDRESS ""

/* To enable direct connectivity you need to copy the content of your
   add-on code into the string below. */
static const char* directConnectivityAddOnCode = "";

/* For direct connectivity IP connections you must provide the server's IP host address
   and port number. Either edit the macros below OR provide these connection
   details on the command line.
   The default direct connectivity IP port number can be specified below by using:
   #define IP_PORT VNC_DIRECT_UDP_DEFAULT_PORT
   Ignore these macros if you are not using the direct connectivity add-on */
#define HOST_ADDRESS ""
#define IP_PORT 0

/* The value of this flag is set automatically according to the user-supplied
   command line arguments and macro definitions above. Cloud connectivity is
   presumed by default here. */
bool usingCloud = true;

/* 
 * EventLoop callbacks
 * We maintain three sets of file descriptors for which we require notifications
 * of readability, writability and exception status. The eventUpdated callback
 * tells us which notifications are needed for a particular descriptor, so we
 * can update the sets accordingly. We also keep track of the maximum file 
 * descriptor value, which, along with the three fd_sets, are used by the
 * select() system call in our event loop.
 */
fd_set fdsRead;
fd_set fdsWrite;
fd_set fdsExcept;
int maxfd = -1;

static void eventUpdated(void* userData, int fd, int eventMask)
{
  if (fd > maxfd) maxfd = fd;
  FD_CLR(fd, &fdsRead);
  if (eventMask & vnc_EventLoopFd_Read) FD_SET(fd, &fdsRead);
  FD_CLR(fd, &fdsWrite);
  if (eventMask & vnc_EventLoopFd_Write) FD_SET(fd, &fdsWrite);
  FD_CLR(fd, &fdsExcept);
  if (eventMask & vnc_EventLoopFd_Except) FD_SET(fd, &fdsExcept);
}

/* Function prototypes */
bool parseCommandLine(int argc, const char** argv,
                      const char** localCloudAddress,
                      const char** localCloudPassword,
                      const char** peerCloudAddress,
                      int* ipPort, const char** directConnectivityHostAddress);
bool initializeSDKandAddOns();
bool initializeFileDescriptorSets();
Display* initializeX11Display(int* fd);
void usageAdvice();
void showSDKError(const char* errorString);
void runEventLoop(int xFd, Display* dpy,
                  BasicViewerWindow* win,
                  vnc_Viewer* viewer);
bool makeCloudConnection(const char* localCloudAddress,
                         const char* localCloudPassword,
                         const char* peerCloudAddress,
                         vnc_Viewer* viewer);
bool makeDirectUdpConnection(const char* hostAddress, int port,
                             vnc_Viewer* viewer);


/*
 * main function - validates cloud addresses, initializes the SDK and the
 * viewer, creates connection handler
 */
int main(int argc, const char **argv)
{
  int exitCode = 1;

  /* Parameter initialisation */
  const char* localCloudAddress = LOCAL_CLOUD_ADDRESS;
  const char* localCloudPassword = LOCAL_CLOUD_PASSWORD;
  const char* peerCloudAddress = PEER_CLOUD_ADDRESS;

  vnc_Viewer* viewer = 0;
  BasicViewerWindow* win = 0;

  /* These are only relevant if you are using the direct connectivity add-on */
  const char* hostAddress = HOST_ADDRESS;
  int port = IP_PORT;

  /* Parse command line */
  if (!parseCommandLine(argc, argv,
                        &localCloudAddress, &localCloudPassword,
                        &peerCloudAddress,
                        &port, &hostAddress)) {
    return exitCode;
  }

  /* Create a logger which outputs to stderr. */
  vnc_Logger_createStderrLogger();

  /* Create a file DataStore for storing persistent data for the viewer.
     Ideally this would be created in a directory that only the viewer
     user has access to. */
  if (!vnc_DataStore_createFileStore("dataStore.txt")) {
    showSDKError("Failed to create data store");
    return exitCode;
  }

  /* Initialize SDK and optional Add-Ons */
  if (initializeSDKandAddOns()) {

    /* Initialize file descriptor sets and associated callback */
    if (initializeFileDescriptorSets()) {
      /* Initialize the X11 display */
      int xFd = -1;
      Display* dpy = initializeX11Display(&xFd);
      if (dpy) {
        /* Create the viewer and window */
        if (!(viewer = vnc_Viewer_create())) {
          showSDKError("Failed to create viewer");
        }
        else {
          win = new BasicViewerWindow(dpy, viewer);

          /* Make a connection to the server */
          if (usingCloud) {
            if (makeCloudConnection(localCloudAddress, localCloudPassword,
              peerCloudAddress, viewer)) {
              exitCode = 0;
            }
          }
          else {
            if (makeDirectUdpConnection(hostAddress, port, viewer)) {
              exitCode = 0;
            }
          }

          if (exitCode == 0) {
            /* Connection object has been constructed */
            runEventLoop(xFd, dpy, win, viewer);
          }
  
          delete win;
        }
        XCloseDisplay(dpy);
      }
    }
  }

  /* Shutdown the SDK */
  vnc_shutdown();
  return exitCode;
}

/*
 * Provide usage information on console.
 */
void usageAdvice()
{
  std::cerr << "You must provide valid connection details." << std::endl;
  std::cerr << "Usage: ./basicViewerX11 [localCloudAddress localCloudPassword"
               " peerCloudAddress]  " << std::endl
            << "   or:";
  std::cerr << " ./basicViewerX11 [directIpHostAddress directIpPortNumber]"
            << std::endl;
}

/*
 * Extract port number from command line argument.
 */
int extractPortNum(const char* arg)
{
  char* tailPtr;
  int port = strtol(arg, &tailPtr, 10);
  if (*tailPtr) return 0; /* tailPtr should point to null */
  return port;
}

/*
 * Parse the command line to obtain connectivity details to be used when
 * listening for incoming connections. A simplistic approach is adopted:
 *
 *   3 arguments - Cloud connectivity to be used
 *                 [localCloudAddress localCloudPassword peerCloudAddress]
 *
 *   2 arguments - direct connectivity to be used
 *                 [directIpHostAddress directIpPortNumber]
 *
 *   0 arguments - the built-in macros must be set appropriately
 */
bool parseCommandLine(int argc, const char** argv,
                      const char** localCloudAddress,
                      const char** localCloudPassword,
                      const char** peerCloudAddress,
                      int* ipPort, const char** directConnectivityHostAddress)
{
  bool badArgs = false;

  /* Parse any supplied command line arguments */
  if (argc == 4 || argc == 3 || argc == 1) {
    if (argc == 4) {  /* Cloud arguments */
      *localCloudAddress = argv[1];
      *localCloudPassword = argv[2];
      *peerCloudAddress = argv[3];
    } else  if (argc == 3) {  /* direct connectivity arguments */
      *directConnectivityHostAddress = argv[1];
      *ipPort = extractPortNum(argv[2]);
      usingCloud = false;
    } else { /* Examine the initial values set by macros */
      if (**localCloudAddress || **localCloudPassword || **peerCloudAddress)
        usingCloud = true;
      else if (*ipPort || **directConnectivityHostAddress)
        usingCloud = false;
    }

    /* Check if all required connectivity details are provided */
    if (usingCloud && (!**localCloudAddress ||
                       !**localCloudPassword ||
                       !**peerCloudAddress)) {
      badArgs = true;
    } else if (!usingCloud && (!*ipPort || !**directConnectivityHostAddress)) {
      badArgs = true;
    }
  } else badArgs = true; /* Invalid number of arguments */

  if (badArgs) {
    usageAdvice();
    return false;
  }
  return true;
}

/*
 * Initialize SDK and Add-ons
 */
bool initializeSDKandAddOns()
{
  /* Initialize the SDK */
  if (!vnc_init()) {
    showSDKError("Failed to initialize VNC SDK");
    return false;
  }

  /* Enable direct connectivity Add-On */
  if (!usingCloud && !vnc_enableAddOn(directConnectivityAddOnCode)) {
    showSDKError("Failed to enable direct connectivity add-on");
    return false;
  }

  return true;
}

/*
 * Initialize File Descriptor Sets & Callback
 */
bool initializeFileDescriptorSets()
{
  FD_ZERO(&fdsRead);
  FD_ZERO(&fdsWrite);
  FD_ZERO(&fdsExcept);
  const vnc_EventLoopFd_Callback eventLoopCallback = {
    eventUpdated,
    0 /* timerUpdated not used here */
  };

  if(!vnc_EventLoopFd_setCallback(&eventLoopCallback, 0))
  {
    showSDKError("Call to vnc_EventLoopFd_setCallback failed");
    return false;
  }
  return true;
}

/*
 * Initialize X11 display and associated File descriptor.
 */
Display* initializeX11Display(int* fd)
{
  /* Open the X11 display and add the corresponding fd to the read set. This
     ensures that the event loop is woken up when any X11 events occur. */
  Display* dpy = XOpenDisplay(0);
  if (dpy) {
    *fd = ConnectionNumber(dpy);
    maxfd = *fd;
    FD_SET(*fd, &fdsRead);
  } else {
    std::cerr << "Failed to open X11 display" << std::endl;
  }
  return dpy;
}

/*
 * Make a Cloud connection
 */
bool makeCloudConnection(const char* localCloudAddress,
                         const char* localCloudPassword,
                         const char* peerCloudAddress,
                         vnc_Viewer* viewer)
{
  vnc_CloudConnector* cloudConnector = 0;
  /* Create connector */
  if (!(cloudConnector = vnc_CloudConnector_create(localCloudAddress,
                                             localCloudPassword))) {
    showSDKError("Failed to create Cloud connector");
    return false;
  }
  /* Connect*/
  std::cout << "Connecting via VNC Cloud, local address: " << localCloudAddress
            << " peer address: " << peerCloudAddress << std::endl;
  if (!vnc_CloudConnector_connect(cloudConnector, peerCloudAddress,
                                  vnc_Viewer_getConnectionHandler(viewer))) {
    showSDKError("Failed to make VNC Cloud connection");
    vnc_CloudConnector_destroy(cloudConnector);
    return false;
  }
  vnc_CloudConnector_destroy(cloudConnector); /* Connector no longer required */
  return true;
}

/*
 * Make a direct connectivity IP connection.
 * Ignore this if you do not intend to use the direct connectivity add-on
 */
bool makeDirectUdpConnection(const char* hostAddress,
                             int port,
                             vnc_Viewer* viewer)
{
  vnc_DirectUdpConnector* udpConnector = 0;
  /* Create direct connectivity UDP connector */
  if (!(udpConnector = vnc_DirectUdpConnector_create())) {
    showSDKError("Failed to create direct UDP connector");
    return false;
  }
  /* Connect */
  std::cout << "Connecting to host address: " << hostAddress
            << " port: " << port << std::endl;

  if (!vnc_DirectUdpConnector_connect(udpConnector, hostAddress, port,
                                      vnc_Viewer_getConnectionHandler(viewer))) {
    showSDKError("Failed to start connection");
    vnc_DirectUdpConnector_destroy(udpConnector);
    return false;
  }
  vnc_DirectUdpConnector_destroy(udpConnector);
  return true;
}

/*
 * Event loop
 */
void runEventLoop(int xFd, Display* dpy,
                  BasicViewerWindow* win, vnc_Viewer* viewer)
{
  /* Run the event loop while the window is open */
  int nextExpiry = 0;
  while (vnc_Viewer_getConnectionStatus(viewer) != vnc_Viewer_Disconnected) {
    /* Make a copy of the fd sets since these get updated by select */
    fd_set selRead = fdsRead;
    fd_set selWrite = fdsWrite;
    fd_set selExcept = fdsExcept;

    /* Calculate timeout if timer is active */
    timeval* timeout = 0;
    timeval delta;
    if (nextExpiry >= 0) {
      delta.tv_sec = nextExpiry / 1000;
      delta.tv_usec = 1000 * (nextExpiry % 1000);
      timeout = &delta;
    }

    /* Wait for events or timeout */
    int ready = select(maxfd+1, &selRead, &selWrite, &selExcept, timeout);

    /* Mark any fd events that occurred */
    if (ready > 0) {
      for (int fd=0; fd<=maxfd; ++fd) {
        if (fd == xFd) continue;
        if (FD_ISSET(fd, &selRead)) {
            vnc_EventLoopFd_markEvents(fd, vnc_EventLoopFd_Read);
        }
        if (FD_ISSET(fd, &selWrite)) {
          vnc_EventLoopFd_markEvents(fd, vnc_EventLoopFd_Write);
        }
        if (FD_ISSET(fd, &selExcept)) {
          vnc_EventLoopFd_markEvents(fd, vnc_EventLoopFd_Except);
        }
      }
    }

    /* Handle any pending X11 events */
    while (XPending(dpy)) {
      XEvent xe;
      XNextEvent(dpy, &xe);
      win->handleXEvent(&xe);
    }

    /* Handle fd events or timers */
    nextExpiry = vnc_EventLoopFd_handleEvents();
  }
}

/*
 * Provide SDK error information on the console.
 */
void showSDKError(const char* errorString)
{
  std::cerr << errorString << ": " << vnc_getLastError() << std::endl;
}
