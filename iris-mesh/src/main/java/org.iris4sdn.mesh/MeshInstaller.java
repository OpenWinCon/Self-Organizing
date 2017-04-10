package org.iris4sdn.mesh;

import com.google.common.collect.Lists;
import org.apache.felix.scr.annotations.*;
import org.onosproject.cli.Comparators;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.net.Device;
import org.onosproject.net.Host;
import org.onosproject.net.device.DeviceEvent;
import org.onosproject.net.device.DeviceListener;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.host.HostEvent;
import org.onosproject.net.host.HostListener;
import org.onosproject.net.host.HostService;
import org.onosproject.net.intent.HostToHostIntent;
import org.onosproject.net.intent.IntentService;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Collections;
import java.util.Date;
import java.util.List;

@Component(immediate = true)
public class MeshInstaller {
    @Reference(cardinality = ReferenceCardinality.OPTIONAL_UNARY)
    protected IntentService intentService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected CoreService coreService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected HostService hostService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DeviceService deviceService;

    private InternalHostListener hostListener = new InternalHostListener();
    private InternalDeviceListener deviceListener = new InternalDeviceListener();

    private List<Host> hosts = Lists.newArrayList(); //host list
    private List<Device> devices = Lists.newArrayList(); //device list
    private ApplicationId appId; //current application id -> get host

    private Boolean deactivate = false;

    //Refresh device & host file (period : 5000ms)
    private Thread infoThread = new Thread(()->{
        try {
            while (!Thread.currentThread().isInterrupted()) {       //////////
                writeHostInfo();
                writeDeviceInfo();
                Thread.sleep(5000);
            }                                                       //////////
        }catch (Exception e){
            if(!deactivate) {
                CLILog("Info Thread Error : " + e.getMessage());
            }
        }
    });

    //executed automatically when the program start
    @Activate
    protected void activate() {
        appId = coreService.registerApplication("org.iris4sdn.mesh");
        hostService.addListener(hostListener);
        deviceService.addListener(deviceListener);

        infoThread.start();

        String command = "python /home/skku/ntl/iris-mesh/src/main/java/org/iris4sdn/mesh/Ch_conf.py";
        shellCmd(command);

        CLILog("Started");
    }

    //executed automatically when the program exit
    @Deactivate
    protected void deactivate() {
        deactivate = true;
        infoThread.interrupt();
        CLILog("Stopped");
    }

    //////////Host information code - start//////////
    private class InternalHostListener implements HostListener {
        @java.lang.Override
        public void event(HostEvent hostEvent) {
            switch (hostEvent.type()) {
                case HOST_ADDED:
                    accConnectivity(hostEvent.subject());
                    hosts.add(hostEvent.subject());
                    break;
                case HOST_REMOVED:
                    break;
                case HOST_UPDATED:
                    break;
                case HOST_MOVED:
                    break;
            }
        }
    }

    //??
    private void accConnectivity(Host host) {
        for (Host dst : hosts) {
            HostToHostIntent intent = HostToHostIntent.builder().appId(appId).one(host.id()).two(dst.id()).build();
            intentService.submit(intent);
        }
    }

    private static List<Host> getSortedHosts(HostService service) {
        List<Host> hosts = Lists.newArrayList(service.getHosts());
        Collections.sort(hosts, Comparators.ELEMENT_COMPARATOR);
        return hosts;
    }

    private void writeHostInfo(){
        try{
            File file = new File("../../ntl/iris-mesh/hostInfo.dat");
            BufferedWriter bw = new BufferedWriter(new FileWriter(file));
            String str = "";

            for(Host host : getSortedHosts(hostService)){
                str += "ID = " + host.id() + "\r\n" +
                        "IPAddr = " + host.ipAddresses() + "\r\n" +
                        "location = " + host.location() + "\r\n" +
                        "MAC = " + host.mac() + "\r\n" +
                        "VLAN = " + host.vlan() + "\r\n\r\n";
            }

            bw.write(str);
            bw.flush();
            bw.close();
        }catch (Exception e){
            CLILog("HostInfo Error : " + e.getMessage());
        }
    }
    //////////end///////////

    //////////Device information code - start//////////
    private class InternalDeviceListener implements DeviceListener {
        @java.lang.Override
        public void event(DeviceEvent event) {
            switch (event.type()) {
                case DEVICE_ADDED:
                    devices.add(event.subject());
                    break;
                case DEVICE_REMOVED:
                    break;
                case DEVICE_UPDATED:
                    break;
            }
        }
    }

    private static List<Device> getSortedDevices(DeviceService service) {
        List<Device> devices = Lists.newArrayList(service.getDevices());
        Collections.sort(devices, Comparators.ELEMENT_COMPARATOR);
        return devices;
    }

    private void writeDeviceInfo(){
        try{
            File file = new File("../../ntl/iris-mesh/deviceInfo.dat");
            BufferedWriter bw = new BufferedWriter(new FileWriter(file));
            String str = "";

            for(Device device : getSortedDevices(deviceService)){
                str += "ManagementAddress = " + device.annotations().value("managementAddress") + "\r\n" +
                        "Available = " + deviceService.isAvailable(device.id()) + "\r\n" +
                        "Role = " + deviceService.getRole(device.id()) + "\r\n" +
                        "ChannelID = " + device.annotations().value("channelId") + "\r\n\r\n";
            }

            bw.write(str);
            bw.flush();
            bw.close();
        }catch (Exception e){
            CLILog("DeviceInfo Error : " + e.getMessage());
        }
    }
    //////////end//////////

    //Execute shell command & show result
    private static void shellCmd(String command){
        try{
            Process process = Runtime.getRuntime().exec(command); //execute shell command
            BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String total = "", result = "";

            while((result = br.readLine()) != null){
                total += result;
            }

            CLILog("Shell command result : " + total);
        }catch (Exception e){
            CLILog("ShellCmd Error : " + e.getMessage());
        }
    }

    //get current time
    private static String getTime(){
        SimpleDateFormat dayTime = new SimpleDateFormat("[hh:mm:ss] ");
        String str = dayTime.format(new Date());
        return str;
    }

    //print CLI console
    public static void CLILog(String str){
        System.out.println(getTime() + str);
    }
}
