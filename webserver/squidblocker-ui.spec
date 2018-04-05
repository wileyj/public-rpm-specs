Name:     squidblocker
Version:  1.0.4
Release:  2%{?dist}
Summary:  The Squid blocker server and client
Epoch:    7
Packager: Eliezer Croitoru <eliezer@ngtech.co.il>
Vendor:   NgTech Ltd
License:  3 Clause BSD
Group:    System Environment/Daemons
URL:      http://www.ngtech.co.il/squidblocker_en.html
Source0:  sbserver.service
Source1:  squidblocker-client
Source2:  squidblocker-server
Source3:  squidblocker-icap-server
Source4:  squidblocker-hub
Source5:  sbhub.service
Source6:  squidblocker-ui.tar.xz
Source7:  htpasswd_default
Source8:  sbserver.sysconfig
Source9:  sbicap.service


Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(preun):  systemd
Requires(postun): systemd
Requires:       systemd-units
# Required to allow debug package auto creation
BuildRequires:  redhat-rpm-config
BuildRequires:  systemd-units

# Required to validate auto requires AutoReqProv: no
## aaaAutoReqProv: no

%description
Squid Blocker for maximum uptime filtering and fast updates.

%prep

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sblocker/
mkdir -p $RPM_BUILD_ROOT/var/squidblocker/ui
mkdir -p $RPM_BUILD_ROOT/var/squidblocker/lists
tar xvf %{SOURCE6} -C $RPM_BUILD_ROOT/var/squidblocker/
install -m 644 %{SOURCE0} ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE5} ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE9} ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/sblocker_client
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/sblocker_http_hub
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}/sblocker_server
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/sblocker_icap
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/sblocker/htpassword
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/sbserver

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(755,root,root) %dir %{_sysconfdir}
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig
%config(noreplace) %{_sysconfdir}/sysconfig/sbserver
%config(noreplace) %{_sysconfdir}/sblocker/htpassword
%attr(755,root,root) %{_sbindir}/sblocker_server
%attr(755,root,root) %{_sbindir}/sblocker_http_hub
%attr(755,root,root) %{_bindir}/sblocker_client
%attr(755,root,root) %{_bindir}/sblocker_icap
%attr(755,root,root) %dir /var/squidblocker/ui
%attr(755,root,root) %dir /var/squidblocker/lists
/var/squidblocker/ui/*

%{_unitdir}/sbserver.service
%{_unitdir}/sbhub.service
%{_unitdir}/sbicap.service

%post
%systemd_post sbserver.service
%systemd_post sbhub.service
%systemd_post sbicap.service

%preun
%systemd_preun sbserver.service
%systemd_preun sbhub.service
%systemd_preun sbicap.service

%postun
%systemd_postun_with_restart sbserver.service
%systemd_postun_with_restart sbhub.service
%systemd_postun_with_restart sbicap.service

%changelog
* Tue Jun 14 2016 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 1.0.4-2 Stable.
+ An improvment to the SquidBlocker-Client external_acl helper.

* Mon Jun 13 2016 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 1.0.4 Stable.
+ Changed the stucture of the lookup code.
+ DeDuplicated multiple instances of the same very long code.
+ Improved error handling on found keys.

* Mon Jun 06 2016 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 1.0.3 Stable.
+ Fixed couple typos in debug output.
+ Added an option to force a prefix on a user or an IP.
+  The key "ip_prefixlink:*" should contain the custom value of the user\ip
+  Prefix such as "all_" to use the prefix "all_dom:*" for the domains blacklists
+  and the "all_url:tcp://*" and all_url:*" urls blacklists.
+  When either no key exist or the key value size is 0 the prefix lookup
+  continues as it like in older versions and verifies the existence of:
+  - ip_dom:*
+  - ip_url:tcp://*

* Wed Jun 01 2016 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 1.0.2 Stable.
+ Fixed couple debug output typos.
+ Added couple interfaces to external domain based filtering,
+  OpenDNS and Symantech. These can be used with SquidBlocker-client.
+ Added support for a custom list for a specific "prefixed" ip or username
+  The default is to use the ip address list if the next keys exitst:
+  - ip_dom:*
+  - ip_url:tcp://*
+  Both are required for a CONNECT request to be used and only the first
+   for full plain https and http urls.
+  See the apis at the UI http://address:port/menu/
- The standalone ICAP service was not upgraded.

* Sun Mar 06 2016 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 1.0.1 Stable.
+ Issue 32 Fixed the DB set_batch to allow it to work with small sizes of lists.
+ Fixed a typo in the .service file

* Thu Jan 21 2016 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 1.0.0 Stable.
 
* Tue Nov 24 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.14 Beta.
- The ICAP service was patched to not break cache manager interface errors when using the "cache_object://" scheme.

* Tue Sep 29 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.13 Beta.
- I have added squidblocker ICAP service which comes to allow these 
- who want to use an ICAP service instead of the external_acl helper interface.

* Thu Sep 24 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.14 Beta.
- Fixed leaked debug output to a running server.

* Wed Sep 16 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.11 Beta.
- Addition of youtube filtering by ID of couple variables such as:
- videoID, listID, userID, channelID.

* Tue Aug 25 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.10 Beta.
- Addition of a systemd HUB VARIABLEs using sysconfig file.
- Fixed the HUB to copy the the full request for each proxy due to an issue with the object.
- Added a "url:*tcp://*:port" lookup before "url:tcp://*" which adds the functionallity to black or white list a single port globally(ipv4 or ipv6).

* Fri Aug 21 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.9 Beta.
- Addition of a systemd VARIABLEs using sysconfig file

* Mon Aug 17 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.8. Beta.
- Fixed a typo in the client logs, it will log into stdout instead of stderr.
- Fixed a typo in the server v6 Tcp check identification.

* Mon Aug 17 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.7. Beta.
- Fixed a typo in the client logs, it will log into stdout instead of stderr.

* Mon Aug 17 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.6. Beta.
- Fixed a typo in the domain check logs

* Mon Aug 17 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.5. Beta.
- Added support for ipv6 host names and CONNECT requests.

* Fri Aug 14 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.4. Beta.
- Fixed a bug in the client.(handling CONNECT method requests better)

* Fri Aug 14 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.3. Beta.
- Changed and fixed couple things in the web pages style.

* Fri Aug 14 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.2. Beta.
- Fixed a typo in the dunno mode.

* Fri Aug 14 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.3.1. Beta.
- Fixing a typo in the systemd service

* Fri Aug 14 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.2.9. Beta.
- Addition of authentication support for server, client and hammer.

* Thu Aug 13 2015 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 0.2.4. Beta.
