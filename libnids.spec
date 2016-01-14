Summary:	E-component of Network Intrusion Detection System
Name:		libnids
Version:	1.24
Release:	1.%{dist}
License:	GPLv2
Vendor: %{vendor}
Packager: %{packager}
Group:		System Environment/Libraries
Source0:	%{name}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Libnids is an implementation of an E-component of Network Intrusion Detection System. It emulates the IP stack of Linux 2.0.x. Libnids offers IP defragmentation, TCP stream assembly and TCP port scan detection.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Libnids library
Requires: %{name} = %{version}

%description devel
Header files needed to develop programs that link against the libnids library.




%prep

%setup -q -n %{name}

%build
git pull 
autoconf
./configure --prefix=%{buildroot}%{_prefix} --libdir=%{buildroot}%{_libdir}
make %{?_smp_mflags}

%install
#mkdir -p %{buildroot}%{_prefix}
make install DESTDIR=%{buildroot}%{_prefix} 

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%{_libdir}/libnids.a
%{_mandir}/man3/libnids.3.gz

%files devel
%{_includedir}/nids.h

%changelog
