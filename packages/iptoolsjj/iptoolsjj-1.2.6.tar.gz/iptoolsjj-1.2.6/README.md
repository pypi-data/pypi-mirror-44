I have written my own python ip/subnet tool. It's for python2/3.
Use theese methods to conver ip mask formats and to check if ip/subnet belong to other subnet.
I made it partly for fun and to learn, so perhaps these are not the best, but they get the job done.
Checking if ip belongs to subnet is actually about 20-30% faster, than with tools from netaddr module.

Methods provided:
- is_in_subnet : check if ip belongs to subnet
- verify : check if ip or ip/netmask are valid
- get_subnet_ip : get subnet ip for some ip/mask
- mask255_to_dec : convert ip mask format
- dec_to_mask255 : convert ip mask format

Instalation:

	pip install iptoolsjj

Import:

	import iptoolsjj

Examples:


Check if 192.168.10.10 is inside 192.168.10.0/22:

	if iptoolsjj.is_in_subnet('192.168.10.10', '192.168.10.0/22'):
    		print ('yes')

Verify if ip or ip with mask is in good format:

	print(iptoolsjj.verify('192.168.1.22'))
	print(iptoolsjj.verify('192.168.1.22/25','ip/mask'))
	print(iptoolsjj.verify('192.168.1.22/255.255.255.128','ip/mask255'))

Get subnet ip for given ip address:

	print(iptoolsjj.get_subnet_ip('191.123.1.36/27'))
			
Convert mask '255.255.255.240' to '28':

	print(iptoolsjj.mask255_to_dec('255.255.255.240'))

Convert mask '28' to '['255', '255', '255', '240']' (normally it's list format):

	print(iptoolsjj.dec_to_mask255(28))

or

	print('.'.join(iptoolsjj.dec_to_mask255(28)))

