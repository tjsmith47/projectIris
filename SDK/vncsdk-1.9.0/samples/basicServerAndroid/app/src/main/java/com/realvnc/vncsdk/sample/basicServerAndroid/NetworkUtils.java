package com.realvnc.vncsdk.sample.basicServerAndroid;

import java.net.*;
import java.util.*;

public class NetworkUtils {

    private static void appendIp(StringBuilder sb, String ip) {
        if (ip.length() > 0) {
            if (sb.length() > 0)
                sb.append(", ");
            sb.append(ip);
        }
    }


    /**
     * Get IP address from first non-localhost interface
     * @param useIPv4   true=return ipv4, false=return ipv6
     * @param returnAll true=return all the addresses, false=return the first address found
     * @return  address or empty string
     */
    public static String getIPAddress(boolean useIPv4, boolean returnAll) {
        StringBuilder sb = new StringBuilder();
        try {
            List<NetworkInterface> interfaces = Collections.list(NetworkInterface.getNetworkInterfaces());
            for (NetworkInterface intf : interfaces) {
                List<InetAddress> addrs = Collections.list(intf.getInetAddresses());
                for (InetAddress addr : addrs) {
                    if (!addr.isLoopbackAddress()) {
                        String sAddr = addr.getHostAddress();
                        boolean isIPv4 = sAddr.indexOf(':')<0;

                        if (useIPv4) {
                            if (isIPv4)
                                appendIp(sb, sAddr);
                        } else {
                            if (!isIPv4) {
                                int delim = sAddr.indexOf('%'); // drop ip6 zone suffix
                                appendIp(sb, delim<0 ? sAddr.toUpperCase() : sAddr.substring(0, delim).toUpperCase());
                            }
                        }

                        if (!returnAll && sb.length() > 0)
                            return sb.toString();
                    }
                }
            }
        } catch (Exception ignored) { } // for now eat exceptions
        return sb.toString();
    }
}
