# $Id$
# Snort.org's SPEC file for Snort

################################################################
# rpmbuild Package Options
# ========================
#
# See pg 399 of _Red_Hat_RPM_Guide_ for rpmbuild --with and --without options.
################################################################

# Other useful bits
%define SnortRulesDir %{_sysconfdir}/snort/rules
%define noShell /bin/false

# Handle the options noted above.
%define for_distro RPMs
%define release 1.%{dist}
%define realname snort


Name: %{realname}
Version: 2.9.7.6
Epoch: 1
Release: %{release}
Summary: An open source Network Intrusion Detection System (NIDS)
Group: Applications/Internet
License: GPL
Packager: %{packager}
Vendor: %{vendor}
Url: http://www.snort.org/
Source0: http://www.snort.org/snort-downloads/2.9.6/%{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf, automake, pcre-devel, libpcap-devel, daq, libdnet-devel, libdnet
#Conflicts: %{conflicts}

%description
Snort is an open source network intrusion detection system, capable of
performing real-time traffic analysis and packet logging on IP networks.
It can perform protocol analysis, content searching/matching and can be
used to detect a variety of attacks and probes, such as buffer overflows,
stealth port scans, CGI attacks, SMB probes, OS fingerprinting attempts,
and much more.

Snort has three primary uses. It can be used as a straight packet sniffer
like tcpdump(1), a packet logger (useful for network traffic debugging,
etc), or as a full blown network intrusion detection system. 

You MUST edit /etc/snort/snort.conf to configure snort before it will work!

There are 5 different packages available. All of them require the base
snort rpm (this one). Additionally, you may need to chose a different
binary to install if you want database support.

If you install a different binary package %{_sbindir}/snort should end up
being a symlink to a binary in one of the following configurations:

	plain		Snort (this package, required)

Please see the documentation in %{_docdir}/%{realname}-%{version} for more
information on snort features and configuration.


%prep
%setup -q -n %{realname}-%{version}

# When building from a Snort.org CVS snapshot tarball, you have to run
# autojunk before you can build.
if [ \( ! -s configure \) -a \( -x autojunk.sh \) ]; then
    ./autojunk.sh
fi

# Make sure it worked, or die with a useful error message.
if [ ! -s configure ]; then
    echo "Can't find ./configure.  ./autojunk.sh not present or not executable?"
    exit 2
fi


%build

BuildSnort() {
   %__mkdir "$1"
   cd "$1"
   %__ln_s ../configure ./configure

   if [ "$1" = "plain" ] ; then
	./configure $SNORT_BASE_CONFIG
   fi

   %__make
   %__mv src/snort ../%{name}-"$1"
   cd ..
}


CFLAGS="$RPM_OPT_FLAGS"
export AM_CFLAGS="-g -O2"
SNORT_BASE_CONFIG="--prefix=%{_prefix} \
                   --bindir=%{_sbindir} \
                   --sysconfdir=%{_sysconfdir}/snort \
                   --with-libpcap-includes=%{_includedir} \
                   --enable-targetbased \
                   --enable-control-socket"

# Always build snort-plain
BuildSnort plain

%install

# Remove leftover CVS files in the tarball, if any...
find . -type 'd' -name "CVS" -print | xargs %{__rm} -rf

InstallSnort() {
   if [ "$1" = "plain" ]; then
	%__rm -rf $RPM_BUILD_ROOT

	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_sbindir}
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_bindir}
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{SnortRulesDir}
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/snort
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_var}/log/snort
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_initrddir}
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_mandir}/man8
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_docdir}/%{realname}-%{version}

	%__install -p -m 0755 %{name}-plain $RPM_BUILD_ROOT%{_sbindir}/%{name}-plain
	%__install -p -m 0755 plain/tools/control/snort_control $RPM_BUILD_ROOT%{_bindir}/snort_control
	%__install -p -m 0755 plain/tools/u2spewfoo/u2spewfoo $RPM_BUILD_ROOT%{_bindir}/u2spewfoo
	%__install -p -m 0755 plain/tools/u2boat/u2boat $RPM_BUILD_ROOT%{_bindir}/u2boat
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicengine
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicpreprocessor
	%__install -p -m 0755 plain/src/dynamic-plugins/sf_engine/.libs/libsf_engine.so.0 $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicengine
	%__ln_s -f %{_libdir}/%{realname}-%{version}_dynamicengine/libsf_engine.so.0 $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicengine/libsf_engine.so
	%__install -p -m 0755 plain/src/dynamic-preprocessors/build/%{_prefix}/lib/snort_dynamicpreprocessor/*.so* $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicpreprocessor
	
    for file in $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicpreprocessor/*.so;  do  
          preprocessor=`basename $file`
          %__ln_s -f %{_libdir}/%{realname}-%{version}_dynamicpreprocessor/$preprocessor.0 $file     
    done   
	
	%__install -p -m 0644 snort.8 $RPM_BUILD_ROOT%{_mandir}/man8
	%__gzip $RPM_BUILD_ROOT%{_mandir}/man8/snort.8
	%__install -p -m 0755 rpm/snortd $RPM_BUILD_ROOT%{_initrddir}
	%__install -p -m 0644 rpm/snort.sysconfig $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/%{realname}
	%__install -p -m 0644 rpm/snort.logrotate $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/snort
	%__install -p -m 0644 etc/reference.config etc/classification.config \
		etc/unicode.map etc/gen-msg.map \
		etc/threshold.conf etc/snort.conf \
		$RPM_BUILD_ROOT/%{_sysconfdir}/snort
	find doc -maxdepth 1 -type f -not -name 'Makefile*' -exec %__install -p -m 0644 {} $RPM_BUILD_ROOT%{_docdir}/%{realname}-%{version} \;

	%__rm -f $RPM_BUILD_ROOT%{_docdir}/%{realname}-%{version}/Makefile.*
    fi
}

# Fix the RULE_PATH
%__sed -e 's;var RULE_PATH ../rules;var RULE_PATH %{SnortRulesDir};' \
	< etc/snort.conf > etc/snort.conf.new
%__rm -f etc/snort.conf
%__mv etc/snort.conf.new etc/snort.conf

# Fix dynamic-preproc paths
%__sed -e 's;dynamicpreprocessor directory \/usr\/local/lib\/snort_dynamicpreprocessor;dynamicpreprocessor directory %{_libdir}\/%{realname}-%{version}_dynamicpreprocessor;' < etc/snort.conf > etc/snort.conf.new
%__rm -f etc/snort.conf
%__mv etc/snort.conf.new etc/snort.conf

# Fix dynamic-engine paths
%__sed -e 's;dynamicengine \/usr\/local/lib\/snort_dynamicengine;dynamicengine %{_libdir}\/%{realname}-%{version}_dynamicengine;' < etc/snort.conf > etc/snort.conf.new
%__rm -f etc/snort.conf
%__mv etc/snort.conf.new etc/snort.conf


# Always install snort-plain
InstallSnort plain

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%pre
# Don't do all this stuff if we are upgrading
if [ $1 = 1 ] ; then
	/usr/sbin/groupadd snort 2> /dev/null || true
	/usr/sbin/useradd -M -d %{_var}/log/snort -s %{noShell} -c "Snort" -g snort snort 2>/dev/null || true
fi

%post
# Make a symlink if there is no link for snort-plain
if [ -L %{_sbindir}/snort ] || [ ! -e %{_sbindir}/snort ] ; then \
	%__rm -f %{_sbindir}/snort; %__ln_s %{_sbindir}/%{name}-plain %{_sbindir}/snort; fi

# We should restart it to activate the new binary if it was upgraded
%{_initrddir}/snortd condrestart 1>/dev/null 2>/dev/null

# Don't do all this stuff if we are upgrading
if [ $1 = 1 ] ; then
	%__chown -R snort.snort %{_var}/log/snort
	/sbin/chkconfig --add snortd
fi


%preun
if [ $1 = 0 ] ; then
	# We get errors about not running, but we don't care
	%{_initrddir}/snortd stop 2>/dev/null 1>/dev/null
	/sbin/chkconfig --del snortd
fi

%postun
# Try and restart, but don't bail if it fails
if [ $1 -ge 1 ] ; then
	%{_initrddir}/snortd condrestart  1>/dev/null 2>/dev/null || :
fi

# Only do this if we are actually removing snort
if [ $1 = 0 ] ; then
	if [ -L %{_sbindir}/snort ]; then
		%__rm -f %{_sbindir}/snort
	fi

	/usr/sbin/userdel snort 2>/dev/null
fi

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/%{name}-plain
%attr(0755,root,root) %{_bindir}/snort_control
%attr(0755,root,root) %{_bindir}/u2spewfoo
%attr(0755,root,root) %{_bindir}/u2boat
%attr(0644,root,root) %{_mandir}/man8/snort.8.*
%attr(0755,root,root) %dir %{SnortRulesDir}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/snort/classification.config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/snort/reference.config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/snort/threshold.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/snort/*.map
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/snort
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/snort/snort.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/snort
%attr(0755,root,root) %config(noreplace) %{_initrddir}/snortd
%attr(0755,snort,snort) %dir %{_var}/log/snort
%attr(0755,root,root) %dir %{_sysconfdir}/snort
%attr(0644,root,root) %{_docdir}/%{realname}-%{version}/*
%attr(0755,root,root) %dir %{_libdir}/%{realname}-%{version}_dynamicengine
%attr(0755,root,root) %{_libdir}/%{realname}-%{version}_dynamicengine/libsf_engine.*
%attr(0755,root,root) %dir %{_libdir}/%{realname}-%{version}_dynamicpreprocessor
%attr(0755,root,root) %{_libdir}/%{realname}-%{version}_dynamicpreprocessor/libsf_*_preproc.*

%dir %{_docdir}/%{realname}-%{version}
%docdir %{_docdir}/%{realname}-%{version}

################################################################
# Thanks to the following for contributions to the Snort.org SPEC file:
#	Henri Gomez <gomez@slib.fr>
#	Chris Green <cmg@sourcefire.com>
#	Karsten Hopp <karsten@redhat.de>
#	Tim Powers <timp@redhat.com>
#	William Stearns <wstearns@pobox.com>
#	Hugo van der Kooij <hugo@vanderkooij.org>
#	Wim Vandersmissen <wim@bofh.be>
#	Dave Wreski <dave@linuxsecurity.com>
#	JP Vossen <jp@jpsdomain.org>
#	Daniel Wittenberg <daniel-wittenberg@starken.com>
#	Jeremy Hewlett <jh@sourcefire.com>
#	Vlatko Kosturjak <kost@linux.hr>

%changelog
