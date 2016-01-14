# Do not forget to bump pam_ssh_agent_auth release if you rewind the main package release to 1
%define openssh_ver 7.1
%define openssh_rel 1.%{dist}
%define pam_ssh_agent_ver 0.9.3
%define pam_ssh_agent_rel 3

# Do we want SELinux & Audit
%if 0%{?!noselinux:1}
%define WITH_SELINUX 1
%else
%define WITH_SELINUX 0
%endif

# OpenSSH privilege separation requires a user & group ID
%define sshd_uid    74
%define sshd_gid    74

# Do we want to disable building of gnome-askpass? (1=yes 0=no)
%define no_gnome_askpass 0

# Do we want to link against a static libcrypto? (1=yes 0=no)
%define static_libcrypto 0

# Use GTK2 instead of GNOME in gnome-ssh-askpass
%define gtk2 1

# Build position-independent executables (requires toolchain support)?
%define pie 1

# Do we want kerberos5 support (1=yes 0=no)
%define kerberos5 1

# Do we want libedit support
%define libedit 1

# Do we want LDAP support
%define ldap 1

# Whether to build pam_ssh_agent_auth
%if 0%{?!nopam:1}
%define pam_ssh_agent 1
%else
%define pam_ssh_agent 0
%endif

# Reserve options to override askpass settings with:
# rpm -ba|--rebuild --define 'skip_xxx 1'
%{?skip_gnome_askpass:%global no_gnome_askpass 1}

# Add option to build without GTK2 for older platforms with only GTK+.
# Red Hat Linux <= 7.2 and Red Hat Advanced Server 2.1 are examples.
# rpm -ba|--rebuild --define 'no_gtk2 1'
%{?no_gtk2:%global gtk2 0}

# Options for static OpenSSL link:
# rpm -ba|--rebuild --define "static_openssl 1"
%{?static_openssl:%global static_libcrypto 1}

# Is this a build for the rescue CD (without PAM, with MD5)? (1=yes 0=no)
%define rescue 0
%{?build_rescue:%global rescue 1}
%{?build_rescue:%global rescue_rel rescue}

# Turn off some stuff for resuce builds
%if %{rescue}
%define kerberos5 0
%define libedit 0
%define pam_ssh_agent 0
%endif

Summary: An open source implementation of SSH protocol versions 1 and 2
Name: openssh
Version: %{openssh_ver}
Release: %{openssh_rel}
URL: http://www.openssh.com/portable.html
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-6.6p1.tar.gz
Source2: sshd.pam
Source3: sshd.init
Source4: http://prdownloads.sourceforge.net/pamsshagentauth/pam_ssh_agent_auth/pam_ssh_agent_auth-%{pam_ssh_agent_ver}.tar.bz2
Source5: pam_ssh_agent-rmheaders
Source6: ssh-keycat.pam
Source7: sshd.sysconfig
Source9: sshd@.service
Source10: sshd.socket
Source11: sshd.service
Source12: sshd-keygen.service
Source13: sshd-keygen

# Internal debug
Patch0: openssh-5.9p1-wIm.patch

#?
Patch100: openssh-6.3p1-coverity.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1872
Patch101: openssh-6.6p1-fingerprint.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1894
#https://bugzilla.redhat.com/show_bug.cgi?id=735889
Patch102: openssh-5.8p1-getaddrinfo.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1889
Patch103: openssh-5.8p1-packet.patch

#https://bugzilla.mindrot.org/show_bug.cgi?id=1402
Patch200: openssh-6.6p1-audit.patch

# --- pam_ssh-agent ---
# make it build reusing the openssh sources
Patch300: pam_ssh_agent_auth-0.9.3-build.patch
# check return value of seteuid()
Patch301: pam_ssh_agent_auth-0.9.2-seteuid.patch
# explicitly make pam callbacks visible
Patch302: pam_ssh_agent_auth-0.9.2-visibility.patch
# don't use xfree (#1024965)
Patch303: pam_ssh_agent_auth-0.9.3-no-xfree.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1641 (WONTFIX)
Patch400: openssh-6.6p1-role-mls.patch
#https://bugzilla.redhat.com/show_bug.cgi?id=781634
Patch404: openssh-6.6p1-privsep-selinux.patch

#?-- unwanted child :(
Patch501: openssh-6.6p1-ldap.patch
#?
Patch502: openssh-6.6p1-keycat.patch

#http6://bugzilla.mindrot.org/show_bug.cgi?id=1644
Patch601: openssh-6.6p1-allow-ip-opts.patch
#http://cvsweb.netbsd.org/cgi-bin/cvsweb.cgi/src/crypto/dist/ssh/Attic/sftp-glob.c.diff?r1=1.13&r2=1.13.12.1&f=h
Patch603: openssh-5.8p1-glob.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1893
Patch604: openssh-6.6p1-keyperm.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1925
Patch606: openssh-5.9p1-ipv6man.patch
#?
Patch607: openssh-5.8p2-sigpipe.patch
#?
Patch608: openssh-6.1p1-askpass-ld.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1789
Patch609: openssh-5.5p1-x11.patch

#?
Patch700: openssh-6.6p1-fips.patch
#?
# drop? Patch701: openssh-5.6p1-exit-deadlock.patch
#?
Patch702: openssh-5.1p1-askpass-progress.patch
#?
Patch703: openssh-4.3p2-askpass-grab-info.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=205842
# drop? Patch704: openssh-5.9p1-edns.patch
#?
Patch705: openssh-5.1p1-scp-manpage.patch
#?
Patch706: openssh-5.8p1-localdomain.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1635 (WONTFIX)
Patch707: openssh-6.6p1-redhat.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1890 (WONTFIX) need integration to prng helper which is discontinued :)
Patch708: openssh-6.6p1-entropy.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1640 (WONTFIX)
Patch709: openssh-6.2p1-vendor.patch
# warn users for unsupported UsePAM=no (#757545)
Patch711: openssh-6.6p1-log-usepam-no.patch
# make aes-ctr ciphers use EVP engines such as AES-NI from OpenSSL
Patch712: openssh-6.3p1-ctr-evp-fast.patch
# add cavs test binary for the aes-ctr
Patch713: openssh-6.6p1-ctr-cavstest.patch


#http://www.sxw.org.uk/computing/patches/openssh.html
#changed cache storage type - #848228
Patch800: openssh-6.6p1-gsskex.patch
#http://www.mail-archive.com/kerberos@mit.edu/msg17591.html
Patch801: openssh-6.6p1-force_krb.patch
Patch900: openssh-6.1p1-gssapi-canohost.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1780
Patch901: openssh-6.6p1-kuserok.patch
# use default_ccache_name from /etc/krb5.conf (#991186)
Patch902: openssh-6.3p1-krb5-use-default_ccache_name.patch
# Run ssh-copy-id in the legacy mode when SSH_COPY_ID_LEGACY variable is set (#969375
Patch905: openssh-6.4p1-legacy-ssh-copy-id.patch
# Use tty allocation for a remote scp (#985650)
Patch906: openssh-6.4p1-fromto-remote.patch
# Try CLOCK_BOOTTIME with fallback (#1091992)
Patch907: openssh-6.4p1-CLOCK_BOOTTIME.patch
# Prevents a server from skipping SSHFP lookup and forcing a new-hostkey
# dialog by offering only certificate keys. (#1081338)
Patch908: openssh-6.6p1-CVE-2014-2653.patch
# OpenSSH 6.5 and 6.6 sometimes encode a value used in the curve25519 key exchange incorrectly
# Disable the curve25519 KEX when speaking to OpenSSH 6.5 or 6.6
Patch909: openssh-5618210618256bbf5f4f71b2887ff186fd451736.patch
# standardise on NI_MAXHOST for gethostname() string lengths (#1051490)
Patch910: openssh-6.6.1p1-NI_MAXHOST.patch

License: BSD
Vendor: %{vendor}
Packager: %{packager}
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: /sbin/nologin
Obsoletes: openssh-clients-fips, openssh-server-fips
Obsoletes: openssh-server-sysvinit

%if ! %{no_gnome_askpass}
%if %{gtk2}
BuildRequires: gtk2-devel
BuildRequires: libX11-devel
%else
BuildRequires: gnome-libs-devel
%endif
%endif

%if %{ldap}
BuildRequires: openldap-devel
%endif
BuildRequires: autoconf, automake, perl, zlib-devel
BuildRequires: audit-libs-devel >= 2.0.5
BuildRequires: util-linux, groff
BuildRequires: pam-devel
BuildRequires: tcp_wrappers-devel
BuildRequires: fipscheck-devel >= 1.3.0
BuildRequires: openssl-devel >= 0.9.8j
#BuildRequires: perl-podlators

%if %{kerberos5}
BuildRequires: krb5-devel
%endif

%if %{libedit}
BuildRequires: libedit-devel ncurses-devel
%endif

%if %{WITH_SELINUX}
Requires: libselinux >= 1.27.7
BuildRequires: libselinux-devel >= 1.27.7
Requires: audit-libs >= 1.0.8
BuildRequires: audit-libs >= 1.0.8
%endif

BuildRequires: xauth

%package clients
Summary: An open source SSH client applications
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Requires: fipscheck-lib%{_isa} >= 1.3.0

%package server
Summary: An open source SSH server daemon
Group: System Environment/Daemons
Requires: openssh = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
Requires: pam >= 1.0.1-3
Requires: fipscheck-lib%{_isa} >= 1.3.0

%if %{ldap}
%package ldap
Summary: A LDAP support for open source SSH server daemon
Requires: openssh = %{version}-%{release}
Group: System Environment/Daemons
%endif

%package keycat
Summary: A mls keycat backend for openssh
Requires: openssh = %{version}-%{release}
Group: System Environment/Daemons

%package askpass
Summary: A passphrase dialog for OpenSSH and X
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Obsoletes: openssh-askpass-gnome
Provides: openssh-askpass-gnome

%package -n pam_ssh_agent_auth
Summary: PAM module for authentication with ssh-agent
Group: System Environment/Base
Version: %{pam_ssh_agent_ver}
Release: %{pam_ssh_agent_rel}.%{openssh_rel}
License: BSD

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features.

This package includes the core files necessary for both the OpenSSH
client and server. To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package includes
the clients necessary to make encrypted connections to SSH servers.

%description server
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
the secure shell daemon (sshd). The sshd daemon allows SSH clients to
securely connect to your SSH server.

%if %{ldap}
%description ldap
OpenSSH LDAP backend is a way how to distribute the authorized tokens
among the servers in the network.
%endif

%description keycat
OpenSSH mls keycat is backend for using the authorized keys in the
openssh in the mls mode.

%description askpass
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH.

%description -n pam_ssh_agent_auth
This package contains a PAM module which can be used to authenticate
users using ssh keys stored in a ssh-agent. Through the use of the
forwarding of ssh-agent connection it also allows to authenticate with
remote ssh-agent instance.

The module is most useful for su and sudo service stacks.

%prep
%setup -q -a 4 -n openssh-6.6p1
#Do not enable by default
%if 0
%patch0 -p1 -b .wIm
%endif

# rework %patch100 -p1 -b .coverity
%patch101 -p1 -b .fingerprint
# investigate %patch102 -p1 -b .getaddrinfo
%patch103 -p1 -b .packet

%if %{pam_ssh_agent}
pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
%patch300 -p1 -b .psaa-build
%patch301 -p1 -b .psaa-seteuid
%patch302 -p1 -b .psaa-visibility
%patch303 -p1 -b .psaa-xfree
# Remove duplicate headers
rm -f $(cat %{SOURCE5})
popd
%endif

%if %{WITH_SELINUX}
%patch400 -p1 -b .role-mls
%patch404 -p1 -b .privsep-selinux
%endif

%if %{ldap}
%patch501 -p1 -b .ldap
%endif
%patch502 -p1 -b .keycat

%patch601 -p1 -b .ip-opts
%patch603 -p1 -b .glob
%patch604 -p1 -b .keyperm
%patch606 -p1 -b .ipv6man
%patch607 -p1 -b .sigpipe
%patch608 -p1 -b .askpass-ld
%patch609 -p1 -b .x11
# 
# drop? %patch701 -p1 -b .exit-deadlock
%patch702 -p1 -b .progress
%patch703 -p1 -b .grab-info
# investigate - https://bugzilla.redhat.com/show_bug.cgi?id=205842
# probably not needed anymore %patch704 -p1 -b .edns
# drop it %patch705 -p1 -b .manpage
%patch706 -p1 -b .localdomain
%patch707 -p1 -b .redhat
%patch708 -p1 -b .entropy
%patch709 -p1 -b .vendor
%patch711 -p1 -b .log-usepam-no
%patch712 -p1 -b .evp-ctr
%patch713 -p1 -b .ctr-cavs
# 
%patch800 -p1 -b .gsskex
%patch801 -p1 -b .force_krb
# 
%patch900 -p1 -b .canohost
%patch901 -p1 -b .kuserok
%patch902 -p1 -b .ccache_name
%patch905 -p1 -b .legacy-ssh-copy-id
%patch906 -p1 -b .fromto-remote
%patch907 -p1 -b .CLOCK_BOOTTIME
%patch908 -p1 -b .CVE-2014-2653
%patch909 -p1 -b .6.6.1
%patch910 -p1 -b .NI_MAXHOST

%patch200 -p1 -b .audit
%patch700 -p1 -b .fips

%if 0
# Nothing here yet
%endif

autoreconf
pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
autoreconf
popd

%build
# the -fvisibility=hidden is needed for clean build of the pam_ssh_agent_auth
# and it makes the ssh build more clean and even optimized better
CFLAGS="$RPM_OPT_FLAGS -fvisibility=hidden -lrt"; export CFLAGS
%if %{rescue}
CFLAGS="$CFLAGS -Os "
%endif
%if %{pie}
%ifarch s390 s390x sparc sparcv9 sparc64
CFLAGS="$CFLAGS -fPIC "
%else
CFLAGS="$CFLAGS -fpic "
%endif
SAVE_LDFLAGS="$LDFLAGS"
LDFLAGS="$LDFLAGS -pie -z relro -z now -lrt"

export CFLAGS
export LDFLAGS

%endif
%if %{kerberos5}
if test -r /etc/profile.d/krb5-devel.sh ; then
        source /etc/profile.d/krb5-devel.sh
fi
krb5_prefix=`krb5-config --prefix`
if test "$krb5_prefix" != "%{_prefix}" ; then
	CPPFLAGS="$CPPFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"
	LDFLAGS="$LDFLAGS -L${krb5_prefix}/%{_lib}"; export LDFLAGS
else
	krb5_prefix=
	CPPFLAGS="-I%{_includedir}/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I%{_includedir}/gssapi"
fi
%endif

%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--datadir=%{_datadir}/openssh \
	--with-tcp-wrappers \
	--with-default-path=/usr/local/bin:/usr/bin \
	--with-superuser-path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin \
	--with-privsep-path=%{_var}/empty/sshd \
	--enable-vendor-patchlevel="FC-%{version}-%{release}" \
	--disable-strip \
	--without-zlib-version-check \
	--with-ssl-engine \
	--with-ipaddr-display \
%if %{ldap}
	--with-ldap \
%endif
%if %{rescue}
	--without-pam \
%else
	--with-pam \
%endif
%if %{WITH_SELINUX}
	--with-selinux --with-audit=linux \
%if 0
#seccomp_filter cannot be build right now
	--with-sandbox=seccomp_filter \
%else
	--with-sandbox=rlimit \
%endif
%endif
%if %{kerberos5}
	--with-kerberos5${krb5_prefix:+=${krb5_prefix}} \
%else
	--without-kerberos5 \
%endif
%if %{libedit}
	--with-libedit
%else
	--without-libedit
%endif

%if %{static_libcrypto}
perl -pi -e "s|-lcrypto|%{_libdir}/libcrypto.a|g" Makefile
%endif

make

# Define a variable to toggle gnome1/gtk2 building.  This is necessary
# because RPM doesn't handle nested %if statements.
%if %{gtk2}
	gtk2=yes
%else
	gtk2=no
%endif

%if ! %{no_gnome_askpass}
pushd contrib
if [ $gtk2 = yes ] ; then
	make gnome-ssh-askpass2
	mv gnome-ssh-askpass2 gnome-ssh-askpass
else
	make gnome-ssh-askpass1
	mv gnome-ssh-askpass1 gnome-ssh-askpass
fi
popd
%endif

%if %{pam_ssh_agent}
pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
LDFLAGS="$SAVE_LDFLAGS"
%configure --with-selinux --libexecdir=/%{_libdir}/security --with-mantype=man
make
popd
%endif

# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    fipshmac -d $RPM_BUILD_ROOT%{_libdir}/fipscheck $RPM_BUILD_ROOT%{_bindir}/ssh $RPM_BUILD_ROOT%{_sbindir}/sshd \
%{nil}

%check
#to run tests use "--with check"
%if %{?_with_check:1}%{!?_with_check:0}
make tests
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ldap.conf

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/sysconfig/
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
install -d $RPM_BUILD_ROOT%{_libdir}/fipscheck
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m644 %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/ssh-keycat
install -m644 %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/sshd
install -m755 %{SOURCE13} $RPM_BUILD_ROOT/%{_sbindir}/sshd-keygen
#install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
#install -m644 %{SOURCE9} $RPM_BUILD_ROOT/%{_unitdir}/sshd@.service
#install -m644 %{SOURCE10} $RPM_BUILD_ROOT/%{_unitdir}/sshd.socket
#install -m644 %{SOURCE11} $RPM_BUILD_ROOT/%{_unitdir}/sshd.service
#install -m644 %{SOURCE12} $RPM_BUILD_ROOT/%{_unitdir}/sshd-keygen.service
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/
install contrib/ssh-copy-id.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install -d $RPM_BUILD_ROOT%{_initrddir}
install contrib/redhat/sshd.init $RPM_BUILD_ROOT%{_initrddir}/sshd

%if ! %{no_gnome_askpass}
install contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/gnome-ssh-askpass
%endif

%if ! %{no_gnome_askpass}
ln -s gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/ssh-askpass
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
%endif

%if %{no_gnome_askpass}
rm -f $RPM_BUILD_ROOT/etc/profile.d/gnome-ssh-askpass.*
%endif

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

%if %{pam_ssh_agent}
pushd pam_ssh_agent_auth-%{pam_ssh_agent_ver}
make install DESTDIR=$RPM_BUILD_ROOT
popd
%endif

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%pre
getent group ssh_keys >/dev/null || groupadd -r ssh_keys || :

%pre server
getent group sshd >/dev/null || groupadd -g %{sshd_uid} -r sshd || :
getent passwd sshd >/dev/null || \
  useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :

%post server

%preun server

%postun server

%triggerun -n openssh-server -- openssh-server < 5.8p2-12
/bin/systemctl enable sshd.service >/dev/null 2>&1
/sbin/chkconfig --del sshd >/dev/null 2>&1 || :
/bin/systemctl try-restart sshd.service >/dev/null 2>&1 || :

%triggerun -n openssh-server -- openssh-server < 5.9p1-22
/bin/systemctl --no-reload disable sshd-keygen.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license LICENCE
%doc CREDITS ChangeLog INSTALL OVERVIEW PROTOCOL* README README.platform README.privsep README.tun README.dns TODO
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%if ! %{rescue}
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%attr(2111,root,ssh_keys) %{_libexecdir}/openssh/ssh-keysign
%attr(0755,root,root) %{_libexecdir}/openssh/ctr-cavstest
%attr(0644,root,root) %{_mandir}/man8/ssh-keysign.8*
%endif

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/ssh
%attr(0644,root,root) %{_libdir}/fipscheck/ssh.hmac
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%attr(0755,root,root) %{_bindir}/scp
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0755,root,root) %{_bindir}/slogin
%attr(0644,root,root) %{_mandir}/man1/slogin.1*
%attr(0644,root,root) %{_mandir}/man5/ssh_config.5*
%if ! %{rescue}
%attr(2111,root,nobody) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_bindir}/sftp
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-pkcs11-helper
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-copy-id.1*
%attr(0644,root,root) %{_mandir}/man8/ssh-pkcs11-helper.8*
%endif

%if ! %{rescue}
%files server
%defattr(-,root,root)
%attr(0755,root,root)  %{_initrddir}/sshd
%dir %attr(0711,root,root) %{_var}/empty/sshd
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_sbindir}/sshd-keygen
%attr(0644,root,root) %{_libdir}/fipscheck/sshd.hmac
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server
%attr(0644,root,root) %{_mandir}/man5/sshd_config.5*
%attr(0644,root,root) %{_mandir}/man5/moduli.5*
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0644,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0640,root,root) %config(noreplace) /etc/sysconfig/sshd
#%attr(0644,root,root) %{_unitdir}/sshd.service
#%attr(0644,root,root) %{_unitdir}/sshd@.service
#%attr(0644,root,root) %{_unitdir}/sshd.socket
#%attr(0644,root,root) %{_unitdir}/sshd-keygen.service
%endif

%if %{ldap}
%files ldap
%defattr(-,root,root)
%doc HOWTO.ldap-keys openssh-lpk-openldap.schema openssh-lpk-sun.schema ldap.conf
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-ldap-helper
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-ldap-wrapper
%attr(0644,root,root) %{_mandir}/man8/ssh-ldap-helper.8*
%attr(0644,root,root) %{_mandir}/man5/ssh-ldap.conf.5*
%endif

%files keycat
%defattr(-,root,root)
%doc HOWTO.ssh-keycat
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-keycat
%attr(0644,root,root) %config(noreplace) /etc/pam.d/ssh-keycat

%if ! %{no_gnome_askpass}
%files askpass
%defattr(-,root,root)
%attr(0644,root,root) %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%attr(0755,root,root) %{_libexecdir}/openssh/gnome-ssh-askpass
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-askpass
%endif

%if %{pam_ssh_agent}
%files -n pam_ssh_agent_auth
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license pam_ssh_agent_auth-%{pam_ssh_agent_ver}/OPENSSH_LICENSE
%attr(0755,root,root) %{_libdir}/security/pam_ssh_agent_auth.so
%attr(0644,root,root) %{_mandir}/man8/pam_ssh_agent_auth.8*
%endif

%changelog
