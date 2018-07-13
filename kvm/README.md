# KVM

## KVM Diagram

![KVM](Kernel-based_Virtual_Machine.svg)

## Libvirt Support

![Libvirt](libvirt_support.svg)

### Adding permissions for using libvirt

- Add user to the libvirt group: `usermod --append --groups libvirt gpoppino`
  - This group is specified in option `unix_sock_group` in `/etc/libvirt/libvirtd.conf`

### Libvirtd daemon

- Check that libvirtd is running: `systemctl status libvirtd`

## KVM Tools

Some of the command line tools are:

- virsh: operate on VMs.
- virt-install: install VMs.
- virt-clone: clone VMs.
- virt-convert: convert a VM from OVF or VMX to native libvirt XML.

Graphical tools are:

- virt-manager: GUI to work with VMs.
- virt-viewer: display a graphical console for a VM.

### Installation of the KVM hypervisor and its tools

- Go to _YaST -> Virtualization -> Install Hypervisor and Tools_
  - Select options _KVM Server_ and _KVM Tools_

### Working with VMs

- List domains (inactive and active): `virsh list --all`
- Obtain information about the VM: `virsh dominfo VM_NAME`
- Start a VM: `virsh start VM_NAME`
- Shutdown a VM: `virsh shutdown VM_NAME`
- Poweroff a VM: `virsh destroy VM_NAME`
- Reboot a VM: `virsh reboot VM_NAME`
- Delete a VM: `virsh undefine VM_NAME; virsh vol-delete --pool default VM_IMAGE.qcow2`

### Configuration

- Edit a VM's config file: `virsh edit VM_NAME`

### Virtual CPU and memory configuration

#### VCPUs

- Check Virtual CPUs of a VM: `virsh vcpuinfo VM_NAME`
- View vcpus configuration: `virsh vcpucount VM_NAME`
- Increment vcpus on a running guest VM and make it permanent (max vcpus must allow this value / --maximum flag): `virsh setvcpus 4 --config --live`

#### Memory

- Set the maximum memory allowed for a VM: `virsh setmaxmem VM_NAME 2048M --config`
- Set increment de memory for a VM: `virsh setmem VM_NAME 2048M --config --live`

### Installation of VMs

- Install a VM: `virt-install --cdrom /path/to/ISO --name "SLES12_SP3" --memory 2048 --virt-type kvm --connect qemu:///system --disk size=10`

### Working with disk images

- Add 5GB to an existing disk image: `qemu-img resize my_image.qcow2 +5G`
- Convert from HyperV to KVM: `qemu-img convert -O qcow2 source.vhdx output_image.qcow2`

### Cloning and Snapshotting

- Clone a VM in a simple way (domain/VM must be paused or shutoff): `virt-clone --original ORIGINAL_VM_NAME --auto-clone`
- Clone a VM with one disk (domain/VM must be paused or shutoff): `virt-clone --connect qemu:///system --original ORIGINAL_VM_NAME --name MY_CLONE --file my_clone.qcow2`
- Take a snapshot of a VM: `virsh snapshot-create-as --domain VM_NAME --name "VM_NAME_SNAPHOST01" --description "My VM_NAME snapshot"`
- List snapshots of a VM: `virsh snapshot-list VM_NAME`
- Revert to a snapshot: `virsh snapshot-revert --domain VN_NAME --snapshotname VM_NAME_SNAPSHOT01 --running`
- Delete an snapshot: `virsh snapshot-delete --domain VM_NAME --snapshotname VM_NAME_SNAPSHOT01`

### Pools

- List pools: `virsh pool-list`
- See pool configuration: `virsh pool-dumpxml POOL_NAME`
- Edit an existing pool configuration: `virsh pool-edit POOL_NAME`
- Create a new pool: `virsh pool-create-as --name mypool --type dir --target /mnt`

### Networking

- List networks: `virsh net-list`
- Edit an existing network: `virsh net-edit NETWORK_NAME`

## Reference

[Official SUSE Documentation for Virtualization on SLES 12](https://www.suse.com/documentation/sles-12/singlehtml/book_virt/book_virt.html)