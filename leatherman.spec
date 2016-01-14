Name:           leatherman
Version:        0.2.0
Release:        1.%{dist}
Summary:        A collection of C++ and CMake utility libraries
Group:          Development/Libraries/C and C++
License:        ASL 2.0
Vendor: 	%{vendor}
Packager: 	%{packager}
URL:            https://puppetlabs.com/%{name}
Source0:        %{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: boost-devel >= 1.59
BuildRequires: openssl-devel libblkid-devel libcurl-devel gcc-c++ make wget tar libyaml libyaml-devel 
Requires:	boost-devel >= 1.59

%description
A collection of C++ and CMake utility libraries

%package devel
Summary:        A collection of C++ and CMake utility libraries
Group:          Development/Libraries/C and C++
Requires:       %{name}

%description devel
Development files for %{name} library.

%prep
%setup -q -n %{name}

%build
git pull

%install
rm -rf %{buildroot}
cmake .
make DESTDIR=%{buildroot} INSTALL="install -p" install

install -d -m 0755 %{buildroot}%{_libdir}
install -d -m 0755 %{buildroot}%{_includedir}
%__mv %{buildroot}/usr/local/include/leatherman %{buildroot}%{_includedir}
%__mv %{buildroot}/usr/local/lib/* %{buildroot}%{_libdir}
%__rm -rf %{buildroot}/usr/local

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%defattr(-,root,root,-)
%dir %{_libdir}/cmake
%dir %{_libdir}/cmake/leatherman
%{_libdir}/cmake/*
%{_libdir}/lib%{name}*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

%changelog
