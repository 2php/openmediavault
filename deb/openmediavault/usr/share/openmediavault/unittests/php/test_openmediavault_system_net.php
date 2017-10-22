#!/usr/bin/phpunit -c/etc/openmediavault
<?php
/**
 * This file is part of OpenMediaVault.
 *
 * @license   http://www.gnu.org/licenses/gpl.html GPL Version 3
 * @author    Volker Theile <volker.theile@openmediavault.org>
 * @copyright Copyright (c) 2009-2017 Volker Theile
 *
 * OpenMediaVault is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * any later version.
 *
 * OpenMediaVault is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with OpenMediaVault. If not, see <http://www.gnu.org/licenses/>.
 */
require_once("openmediavault/autoloader.inc");
require_once("openmediavault/globals.inc");

class NetworkInterfaceMock extends \OMV\System\Net\NetworkInterface {
	public function __construct() {
		parent::__construct("ens6");
		$this->ip = implode("|", [
			"2: ens6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000",
			"    link/ether 52:54:00:a6:76:53 brd ff:ff:ff:ff:ff:ff",
			"    inet 192.168.121.38/24 brd 192.168.121.255 scope global dynamic ens6",
			"       valid_lft 2325sec preferred_lft 2325sec",
			"    inet6 ::ffff:192.168.121.38/64 scope global ",
			"       valid_lft forever preferred_lft forever",
			"    inet6 fe80::5054:ff:fea6:7653/64 scope link ",
			"       valid_lft forever preferred_lft forever"
		]);
	}
}

class test_openmediavault_system_net extends \PHPUnit_Framework_TestCase {
	protected function getNetworkInterfaceMock() {
		return new NetworkInterfaceMock();
	}

	public function test_getIP() {
		$mock = $this->getNetworkInterfaceMock();
		$this->assertEquals($mock->getIP(), "192.168.121.38");
	}

	public function test_getIP6() {
		$mock = $this->getNetworkInterfaceMock();
		$this->assertEquals($mock->getIP6(), "::ffff:192.168.121.38");
	}

	public function test_getPrefix() {
		$mock = $this->getNetworkInterfaceMock();
		$this->assertEquals($mock->getPrefix(), 24);
	}

	public function test_getPrefix6() {
		$mock = $this->getNetworkInterfaceMock();
		$this->assertEquals($mock->getPrefix6(), 64);
	}

	public function test_getMask() {
		$mock = $this->getNetworkInterfaceMock();
		$this->assertEquals($mock->getMask(), "255.255.255.0");
	}

	public function test_getMask6() {
		$mock = $this->getNetworkInterfaceMock();
		$this->assertEquals($mock->getMask6(), 64);
	}
}
