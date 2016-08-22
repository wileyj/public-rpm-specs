%define repo https://github.com/duosecurity/duo_unix.git
%define gitversion %(echo `curl -s https://github.com/duosecurity/duo_unix/releases | grep 'class="tag-name"' | head -1 |  tr -d 'duo_ux</span class="tag-name">-'`)

Name: duo
Version: %{gitversion}
Summary: Duo two-factor authentication for Unix systems
Release: 1.%{?dist}
License: GPLv3
Group: Applications/Security
URL: https://duo.com
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: pam
Requires: openssl
Requires: %{name}-libs = %{version}
BuildRequires: pam-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: openssh-server
BuildRequires: gcc
BuildRequires: git

%description
Duo provides simple two-factor authentication as a service via:

    1.  Phone callback
    2.  SMS-delivered one-time passcodes
    3.  Duo mobile app to generate one-time passcodes
    4.  Duo mobile app for smartphone push authentication
    5.  Duo hardware token to generate one-time passcodes

This package allows an admin (or ordinary user) to quickly add Duo
authentication to any Unix login without setting up secondary user
accounts, directory synchronization, servers, or hardware.

%package -n %{name}-libs
Summary: Shared libraries for duo authentication
Group: System/Libraries

%description -n %{name}-libs
Shared libraries for duo_unix

%package -n %{name}-pam
Summary: A PAM module for duo authentication
Group: System/Libraries
Requires: %{name}-libs = %{version}

%description -n %{name}-pam
A PAM module for duo authentication

%package -n %{name}-devel
Summary: Development files and documentation for duo_unix
Group: System/Libraries
Requires: %{name}-libs = %{version}

%description -n %{name}-devel
Development files and documentation for duo_unix

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
./bootstrap
%configure \
  --with-pam=%{_lib}/security \
  --sysconfdir=%{_sysconfdir}/duo \
  --with-privsep-user=sshd \
  --includedir=%{_includedir}/duo \
  --docdir=%{_datadir}/doc/%{name}

make %{?_smp_mflags}

%install
cd %{name}-%{version}
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_lib}/security/pam_duo.*a
%{__cat} <<EOF >${RPM_BUILD_ROOT}%{_sysconfdir}/duo/login_duo.conf
[duo]
ikey = key
skey = secret
host = api-bc5aebab.duosecurity.com
pushinfo=yes
autopush=yes
EOF

%post -n %{name}-libs -p /sbin/ldconfig

%postun -n %{name}-libs -p /sbin/ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/duo
%attr(0600, sshd, root) %config(noreplace) %{_sysconfdir}/duo/login_duo.conf
%attr(4755, root, root) %{_sbindir}/login_duo
%{_mandir}/man8/login_duo.8.gz
%{_defaultdocdir}/%{name}/AUTHORS
%{_defaultdocdir}/%{name}/CHANGES
%{_defaultdocdir}/%{name}/LICENSE
%{_defaultdocdir}/%{name}/README
#   %{_datadir}/doc/%{name}/AUTHORS

%files -n %{name}-pam
%dir %{_sysconfdir}/duo
/%{_lib}/security/pam_duo.so
%config(noreplace) %attr(640, root, root) %{_sysconfdir}/duo/pam_duo.conf
%{_mandir}/man8/pam_duo.8.gz

%files -n %{name}-libs
%defattr(-,root,root)
%{_libdir}/libduo.so*

%files -n %{name}-devel
%defattr(-,root,root)
%{_libdir}/libduo.a
%{_libdir}/libduo.la
%{_includedir}/duo/duo.h
%{_includedir}/duo/util.h
%{_libdir}/pkgconfig/libduo.pc
%{_mandir}/man3/duo.3.gz

%changelog
