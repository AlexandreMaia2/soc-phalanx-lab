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


## VLAN 20 - Administration Network

The first segmented network created in the SOC PHALANX lab is VLAN 20, dedicated to administrative endpoints.

### VLAN Configuration

| Setting | Value |
|---|---|
| VLAN ID | 20 |
| Interface | ADMIN |
| Network | 10.20.20.0/24 |
| Gateway | 10.20.20.1 |
| DHCP Range | 10.20.20.100 - 10.20.20.199 |

The pfSense interface `10.20.20.1` acts as the default gateway for hosts connected to the ADMIN network.

The DHCP pool was intentionally limited to `10.20.20.100-199`, leaving addresses outside the dynamic range available for infrastructure, servers, static assignments, and future reservations.

### DHCP Configuration

DHCP was enabled on the ADMIN interface to automatically provide network configuration to client systems connected to VLAN 20.

![ADMIN VLAN DHCP enabled](../../screenshots/pfsense/06-admin-vlan-dhcp-enabled.png)

The configured DHCP pool distributes addresses between `10.20.20.100` and `10.20.20.199` within the `10.20.20.0/24` subnet.

![ADMIN VLAN DHCP pool](../../screenshots/pfsense/07-admin-vlan-dhcp-pool.png)

### Current Status

- VLAN 20 created and assigned to the ADMIN interface
- Static gateway configured as `10.20.20.1/24`
- DHCP service enabled
- DHCP pool configured as `10.20.20.100-199`
- Client validation pending
- Inter-VLAN firewall rules pending
