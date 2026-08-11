# pfSense Firewall Foundation

## Overview

This document covers the initial pfSense network configuration for the SOC PHALANX lab.

The goal of this stage was to place the Windows Server behind pfSense, making the firewall the gateway between the internal lab network and the external VMware NAT network.


## Network Architecture

pfSense uses two virtual network interfaces:

| Interface | VMware Network |     IP Address     |                 Purpose                  |
|-----------|----------------|--------------------|------------------------------------------|
| WAN (em0) | NAT            | 192.168.240.131/24 | External connectivity through VMware NAT |
| LAN (em1) | Host-only      | 192.168.1.1/24     |            Internal lab network          |

The WAN interface connects pfSense to the external VMware NAT network, while the LAN interface provides the gateway for the isolated internal lab network.


## Initial Problem

The Windows Server was initially connected directly to the VMware NAT network.

Its network configuration was:

| Setting         |       Value       |
|-----------------|-------------------|
| IP Address      | 192.168.240.10/24 |
| Default Gateway |   192.168.240.2   |
|   DNS Server    |       8.8.8.8     |

Because the server was connected to the NAT network instead of the pfSense LAN, it was outside the internal lab network.

As a result, the pfSense WebGUI at `192.168.1.1` could not be reached from the server.



## Correction

The Windows Server network adapter was changed from **NAT** to **Host-only**, placing the server on the internal network connected to the pfSense LAN interface.

The Windows Server was then configured with:

|   Setting  | Value |
|------------|-------|
|   IP Address    | 192.168.1.10/24 |
| Default Gateway | 192.168.1.1 |
|  DNS Server     | 192.168.1.10 |

With this configuration, pfSense (`192.168.1.1`) became the default gateway for the Windows Server.


## Validation

After applying the new network configuration, connectivity between the Windows Server and pfSense was tested with:

`ping 192.168.1.1`

The test returned four successful replies with **0% packet loss**.

The pfSense WebGUI also became accessible from the Windows Server at:

`https://192.168.1.1`

This confirmed that the Windows Server was successfully connected to the internal network behind pfSense.
