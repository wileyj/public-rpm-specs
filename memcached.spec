Summary: Memcached 
Name: memcached
Version: 1.4.5
Release: 1.%{dist}
License: GPL
Vendor: %{vendor}
Packager: %{packager}
Group: web
Source: %{name}-%{version}.tar.gz
Source1: memcached.init
Source2: memcached.sysconfig
BuildRequires: libevent-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
Memcache

%prep
%setup

%build
%configure
make %{?_smp_mflags}
%install
%makeinstall
mkdir -p %{buildroot}/etc/init.d
mkdir -p %{buildroot}/etc/sysconfig
%{__install} -p -m0755 %{SOURCE1} %{buildroot}/etc/init.d/memcached
%{__install} -p -m0644 %{SOURCE2} %{buildroot}/etc/sysconfig/memcached

%post
/sbin/chkconfig --add memcached

%preun
if [ $1 -eq 0 ]; then
  /sbin/service memcached stop &> /dev/null || :
  /sbin/chkconfig --del memcached
fi

%postun
/sbin/service memcached condrestart &>/dev/null || :

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING doc/*.txt NEWS README
%doc %{_mandir}/man1/memcached.1*
%config(noreplace) %{_sysconfdir}/sysconfig/memcached
%config /etc/init.d/memcached
%{_bindir}/memcached
#%{_bindir}/memcached-debug
%{_includedir}/%{name}


