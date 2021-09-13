namespace BasicViewerCSharpWpf
{
    public class ConnectSettings
    {
        public bool UsingCloud { get; set; } = true;

        public string LocalCloudAddress { get; set; }
        public string LocalCloudPassword { get; set; }
        public string PeerCloudAddress { get; set; }

        public string DirectConnectivityAddress { get; set; }
        public int DirectConnectivityIpPort { get; set; }
        public bool LocalCloudIsEditable { get; internal set; }

        public bool SettingsArePresent
        {
            get
            {
                return (!string.IsNullOrWhiteSpace(LocalCloudAddress) &&
                        !string.IsNullOrWhiteSpace(LocalCloudPassword) &&
                        !string.IsNullOrWhiteSpace(PeerCloudAddress)) ||

                        (!string.IsNullOrWhiteSpace(DirectConnectivityAddress) && DirectConnectivityIpPort != 0);
            }
        }
    }
}
