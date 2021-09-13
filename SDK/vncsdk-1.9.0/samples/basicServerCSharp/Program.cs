// Copyright (C) 2016-2020 RealVNC Limited. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice,
// this list of conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright notice,
// this list of conditions and the following disclaimer in the documentation
// and/or other materials provided with the distribution.
//
// 3. Neither the name of the copyright holder nor the names of its contributors
// may be used to endorse or promote products derived from this software without
// specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

//This file contains the basicServerCsharp sample.
//
//Usage:
//    basicServerCsharp [LOCAL_CLOUD_ADDRESS][LOCAL_CLOUD_PASSWORD]
//                                [IP_PORT]
//
//Arguments:
//    LOCAL_CLOUD_ADDRESS   - the VNC Cloud address for this Server
//    LOCAL_CLOUD_PASSWORD  - the VNC Cloud password for this Server
//    IP_PORT               - Direct IP Connectivity port number
//
//    All arguments may be omitted if they have been hard-coded in this file.
//
//This sample shows how to implement a basic VNC server using the C# bindings
//for the VNC SDK.
//
//Two types of connectivity are supported: Cloud-based and direct connectivity (UDP or TCP),
//with the server permitted to use both mechanisms concurrently.
//
//Note: To use direct connectivity you will need to apply an add-on code; a trial
//code is available from your RealVNC account.You can ignore direct connectivity related
//code below if you do not intend to use the direct connectivity add-on.
//
//The server listens for incoming connections using connectivity details that
//can be either specified on the command line, or hard-coded by editing this
//C# source file.
//
//Each time it starts, the server generates a new random 4-digit password and
//prints this to the console. A viewer must specify this password when prompted
//in order to successfully connect.

using System;
using System.IO;
using System.Runtime.InteropServices;
using RealVNC.VncSdk;

namespace BasicServerCSharp
{
    class Program
    {
        // For Cloud connections, either hard-code the Cloud address for the Server OR
        // specify it at the command line. Example Cloud address:
        // LxygGgSrhXQFiLj5M4M.LxyPXzA9sGLkB6pCtJv.devEX1Sg2Txs1CgVuW4.LxyPRsVnXoDoue4Xqm
        const string LOCAL_CLOUD_ADDRESS = "";

        // Either hard-code the Cloud password associated with this Cloud address OR
        // specify it at the command line. Example Cloud password: KMDgGgELSvAdvscgGfk2
        const string LOCAL_CLOUD_PASSWORD = "";

        // To enable Direct IP Connectivity (UDP or TCP) you need to copy the content of your
        // add-on code into the string below.
        const string DIRECT_CONNECTIVITY_ADD_ON_CODE = "";

        // For direct connectivity you must provide an IP listening port number.
        // Either edit IP_PORT variable below OR provide the port number on the command
        // line. The default direct connectivity IP port number can be specified below by using:
        // IP_PORT = vncsdk.DirectUdp.DEFAULT_PORT
        // Ignore this if you are not using the direct connectivity add-on
        const int IP_PORT = 0;

        // The following flags indicate the type of connection(s) being used and they
        // are set automatically according to user-supplied command line arguments and
        // the macro definitions above. Each type of connection is optional.
        // If you set any flag to true below then that makes that type of connection
        // mandatory i.e. connectivity details MUST be provided via the command line or
        // via hard-coded values from global variables above.
        static bool usingCloud = false;
        static bool usingDirectConnectivity = false;

        // Number of random digits in the auto-generated server password:
        const int SERVER_PASSWORD_LENGTH = 4;

        static string localCloudAddress = LOCAL_CLOUD_ADDRESS;
        static string localCloudPassword = LOCAL_CLOUD_PASSWORD;
        static string directConnectivityAddOnCode = DIRECT_CONNECTIVITY_ADD_ON_CODE;
        static int ipPort = IP_PORT;

        static void UsageAdvice()
        { //Provide usage information on console.
            Console.Error.WriteLine("Usage:  basicCsharpServer [cloudAddress cloudPassword] " +
                                    "[directConnectivityPortNumber]");
            Console.ReadKey();
        }


        static bool ParseCommandLine(string[] args)
        { //Parse the command line to obtain connectivity details to be used when
          //listening for incoming connections.A simplistic approach is adopted:
          //
          //3 arguments - Cloud and direct connectivity to be used
          //              [LOCAL_CLOUD_ADDRESS LOCAL_CLOUD_PASSWORD] [IP_PORT]
          //
          //2 arguments - Cloud connectivity to be used
          //              [LOCAL_CLOUD_ADDRESS LOCAL_CLOUD_PASSWORD]
          //
          //1 argument  - direct connectivity to be used
          //              [IP_PORT]
          //
          //0 arguments - the built-in macros must be set appropriately

            bool badArgs = false;

            // Parse any supplied command line arguments
            switch (args.Length) {
                case 3: //Cloud and direct connectivity arguments
                    localCloudAddress = args[0];
                    localCloudPassword = args[1];
                    usingCloud = usingDirectConnectivity = true;
                    Int32.TryParse(args[2], out ipPort);
                    break;
                case 2: //Cloud arguments only
                    localCloudAddress = args[0];
                    localCloudPassword = args[1];
                    usingCloud = true;
                    break;
                case 1: //direct connectivity argument only
                    usingDirectConnectivity = true;
                    Int32.TryParse(args[0], out ipPort);
                    break;
                case 0: //Examine initial values
                    if (localCloudAddress.Length > 0 || localCloudPassword.Length > 0)
                        usingCloud = true;
                    if (ipPort > 0)
                        usingDirectConnectivity = true;
                    break;
                default:
                    badArgs = true;
                    break;
            }
            if (!badArgs) {
                // Check if all required connectivity details are provided either via
                // editing the global variables above, or on the command-line
                if (usingCloud && (localCloudAddress.Length == 0 || localCloudPassword.Length == 0)) {
                    Console.Error.WriteLine("You must provide a valid Cloud address and password");
                    badArgs = true;
                }
                if (usingDirectConnectivity && ipPort == 0) {
                    Console.Error.WriteLine("You must provide a valid IP port number");
                    badArgs = true;
                }
                if (!usingCloud && !usingDirectConnectivity) {
                    Console.Error.WriteLine("No connectivity information provided.");
                    badArgs = true;
                }
            }
            if (badArgs) {
                UsageAdvice();
            }
            return !badArgs;
        }

        class SecurityCallback : Server.SecurityCallback
        { //Security callback, used to authenticate incoming connections.
            readonly string password;

            public SecurityCallback()
            {
                password = GeneratePassword();
                Console.Write("Server password is: ");

                // Emphasise PIN with colour
                ConsoleColor old = Console.ForegroundColor;
                Console.ForegroundColor = (old != ConsoleColor.Green && old != ConsoleColor.DarkGreen) ? ConsoleColor.Green : ConsoleColor.Magenta;
                Console.WriteLine("{0}", password);
                Console.ForegroundColor = old;
            }

            protected override bool OnIsUserNameRequired(Server server, Connection connection)
            { //Don't prompt for a username when accessing this server, just a
              //password is required
                return false;
            }

            protected override Server.Permissions OnAuthenticateUser(Server server, Connection connection, string username, string password)
            { //Check that the password supplied by the connecting viewer is the same
              //as the server's auto-generated random password. If so, allow the
              //connection with all permissions, otherwise do not allow the
              //connection.
                return password == this.password ? Server.Permissions.All : Server.Permissions.Zero;
            }

            static string GeneratePassword()
            { // Generate the server password.
                string password = "";
                Random rnd = new Random();
                for (int i = 0; i < SERVER_PASSWORD_LENGTH; ++i) {
                    password += (rnd.Next() % 10).ToString();
                }
                return password;
            }
        };

        // Windows-specific code for console event handling.
        struct NativeMethods
        { // Declare the SetConsoleCtrlHandler function
          // as external and receiving a delegate.
            [DllImport("Kernel32")]
            public static extern bool SetConsoleCtrlHandler(HandlerRoutine Handler, bool Add);
        }

        // A delegate type to be used as the handler routine 
        // for SetConsoleCtrlHandler.
        public delegate bool HandlerRoutine(CtrlTypes CtrlType);

        // An enumerated type for the control messages
        // sent to the handler routine.
        public enum CtrlTypes
        {
            CTRL_C_EVENT = 0,
            CTRL_BREAK_EVENT,
            CTRL_CLOSE_EVENT,
            CTRL_LOGOFF_EVENT = 5,
            CTRL_SHUTDOWN_EVENT
        }

        private static bool ConsoleCtrlCheck(CtrlTypes ctrlType)
        { //Stop the event loop if CTRL-C or CTRL-Break are called or if the console window is closed
            EventLoop.Stop();
            return true;
        }

        /// <summary>
        /// Get the directory containing the VNC SDK dynamic library.
        /// </summary>
        static string GetLibraryDirectory()
        {
#if DEBUG
            // Get the default location of the VNC SDK "lib" directory
            // relative to the executable's build directory.
            var exeDir = AppDomain.CurrentDomain.BaseDirectory;
            var sdkRoot = new DirectoryInfo(exeDir).Parent.Parent.Parent.Parent;
            var libDir = Path.Combine(sdkRoot.FullName, "lib");

            // Return the appropriate platform-specific subdirectory.
            return DynamicLoader.GetPlatformSubdirectory(libDir);
#else
        // This is intentionally not meant to compile.
        // EDIT AS APPROPRIATE
        // Production applications should return a trusted directory,
        // which will depend on details of how the application will be
        // deployed.
        return secureDirectoryFullPath;
#endif
        }

        class ServerConnectionCallback : Server.ConnectionCallback
        {
            protected override void OnConnectionStarted(Server s, Connection c)
            {
                Console.WriteLine("Viewer {0} connected", s.GetPeerAddress(c));
            }
            protected override void OnConnectionEnded(Server s, Connection c)
            {
                Console.WriteLine("Viewer {0} disconnected", s.GetPeerAddress(c));
            }
        }

        class CloudListenerCallback : CloudListener.Callback
        {
            protected override void OnListeningStatusChanged(CloudListener listener, CloudListener.Status status)
            {
                if (status == CloudListener.Status.Searching) {
                    Console.WriteLine("The listener is in the process of establishing " +
                                      "an association with VNC Cloud");
                }
                else {
                    Console.WriteLine("Listening for VNC Cloud connections");
                }
            }

            protected override void OnListeningFailed(CloudListener listener, string cloudError, int retryTimeSecs)
            {
                EventLoop.Stop();
                Console.WriteLine("VNC Cloud listening error: {0}", cloudError);
            }
        }

        class RsaKeyCallback : RsaKey.Callback
        {
            //RsaKey callback - key details ready
            protected override void OnDetailsReady(ImmutableDataBuffer rsaPublic, string hexFingerprint, string catchphraseFingerprint)
            {
                Console.WriteLine("Server id is: {0}", hexFingerprint);
                Console.WriteLine("Server catchphrase is: {0}", catchphraseFingerprint);
            }
        }

        /// This is true if the application is running on Windows.
        static readonly bool isWindows =
          (int)Environment.OSVersion.Platform != 4 &&
          (int)Environment.OSVersion.Platform != 6 &&
          (int)Environment.OSVersion.Platform != 128;

        static void Main(string[] args)
        {

            if (ParseCommandLine(args)) {
                try {
                    // Load the VNC SDK dynamic library.
                    string libDir = Path.GetFullPath(GetLibraryDirectory());
                    string dllPath = DynamicLoader.LoadLibrary(libDir);

                    // Set the directory containing vncagent.
                    string vncAgentPath = Path.GetDirectoryName(dllPath);

                    // Create a logger which outputs to sys.stderr
                    Logger.CreateStderrLogger();

#if DEBUG
                    // Not recommended for release builds. Enabling "full" logging is useful for seeing what's
                    // going on when first trying a system. See Logger.h for more details
                    Logger.SetLevel(Logger.Level.Full);
#endif

                    // Create a file DataStore for storing persistent data for the server.
                    // Ideally this would be created in a directory that only the server
                    // user has access to.
                    DataStore.CreateFileStore("fileStore.txt");

                    try {
                        // Initialize SDK and optional Add-Ons
                        Library.Init();
                        if (usingDirectConnectivity)
                            Library.EnableAddOn(directConnectivityAddOnCode);

                        Server server = new Server(vncAgentPath);
                        server.SetConnectionCallback(new ServerConnectionCallback());

                        SecurityCallback securityCallback = new SecurityCallback();
                        server.SetSecurityCallback(securityCallback);

                        // Listen on each transport that we intend to use.
                        if (usingCloud) {
                            Console.WriteLine("Signing in to VNC Cloud");
                            CloudListener cloudListener = new CloudListener(localCloudAddress, localCloudPassword, server.GetConnectionHandler(), new CloudListenerCallback());
                        }

                        if (usingDirectConnectivity) {
                            //Start listening for connections made via direct connectivity
                            //Ignore this if you do not intend to use the direct connectivity add-on.
                            Console.WriteLine("Listening for direct connections");

                            //This is a do nothing callback. It may not be needed.
                            DirectUdpListener.Callback listenerCallback = new DirectUdpListener.Callback();
                            DirectUdpListener listener = new DirectUdpListener(ipPort, string.Empty, server.GetConnectionHandler(), listenerCallback);

                            //If DirectUdp is being used, request the RSA key details to
                            //display so that viewers can verify they are connecting to this
                            //server.
                            RsaKey.GetDetails(new RsaKeyCallback(), true);
                        }

                        if (isWindows) {
                            //Register handler to stop event loop if CTRL-C, CTRL-Break or console window closed.
                            NativeMethods.SetConsoleCtrlHandler(new HandlerRoutine(ConsoleCtrlCheck), true);
                        }

                        // Server setup complete, now run the EventLoop.
                        EventLoop.Run();
                    }
                    finally {
                        if (isWindows) {
                            //Unregister the console control handler
                            NativeMethods.SetConsoleCtrlHandler(null, false);
                        }
                        Library.Shutdown();
                    }
                }
                catch (Exception e) {
                    Console.Error.WriteLine("Exception: {0}", e.Message);
#if DEBUG
                    Console.Error.WriteLine(e.StackTrace);
#endif
                }
            }
        }
    }
}
