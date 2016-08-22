Name:       unbound
Version:    1.5.9
Release:    1.%{dist}
Summary:    Unbound is a validating, recursive, and caching DNS resolver. 
Group:      System Environment/Libraries
License:    BSD
URL:        https://unbound.nlnetlabs.nl
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  make gcc
Requires:	%{name}-libs = %{version}

%description
%{name}  is a validating, recursive, and caching DNS resolver.
The C implementation of Unbound is developed and maintained by NLnet Labs. It is based on ideas and algorithms taken from a java prototype developed by Verisign labs, Nominet, Kirei and ep.net.
Unbound is designed as a set of modular components, so that also DNSSEC (secure DNS) validation and stub-resolvers (that do not run as a server, but are linked into an application) are easily possible.

%package devel
Summary:    Development headers and library for %{name}
Group:      Development/Libraries
Requires:   %{name}-libs = %{version}

%description devel
This package contains the development headers and library for %{name}.

%package libs
Summary:  Library package for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}

%description libs
THis package contains the libraries for %{name}

%package doc
Summary:    Documentation for %{name}
Group:      Documentation
BuildArch:  noarch

%description doc
This package contains the documentation for %{name}

%prep
%setup -q 

%build
%configure
make %{_smp_mflags}
find doc -type f -exec chmod 0644 \{\} \;

%install
rm -fr %{buildroot}
make install DESTDIR=%{buildroot}

%post 
getent group %{name} &>/dev/null || groupadd -r %{name} -g 55 &>/dev/null
getent passwd %{name} &>/dev/null || useradd -r -u 55 -g %{name} -d /dev/null -s /sbin/nologin -c %{name} %{name} &>/dev/null
if [ $1 -gt 1 ] ; then
  usermod -d /dev/null %{name} &>/dev/null
fi

%postun 
groupdel %{name} &>/dev/null
userdel %{name} &>/dev/null

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/%{name}*
%{_sysconfdir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf

%files libs
%defattr(-,root,root)
%{_libdir}/lib%{name}*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}.h

%files doc
%defattr(-,root,root)
%doc %{_mandir}/man1/%{name}*
%doc %{_mandir}/man3/lib%{name}*
%doc %{_mandir}/man3/ub_*
%doc %{_mandir}/man5/%{name}*
%doc %{_mandir}/man8/%{name}*

