%define repo https://github.com/puppetlabs/leatherman.git

Name:           leatherman
Version:        0.2.0
Release:        1.%{dist}
Summary:        A collection of C++ and CMake utility libraries
Group:          Development/Libraries/C and C++
License:        ASL 2.0
Vendor: 	%{vendor}
Packager: 	%{packager}
URL:            https://puppetlabs.com/%{name}
#Source0:        %{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: boost-devel >= 1.59
BuildRequires: openssl-devel libblkid-devel libcurl-devel gcc-c++ make wget tar libyaml libyaml-devel 
Requires:	boost-devel >= 1.59
BuildArch:	noarch

%description
A collection of C++ and CMake utility libraries

%package devel
Summary:        A collection of C++ and CMake utility libraries
Group:          Development/Libraries/C and C++
Requires:       %{name}

%description devel
Development files for %{name} library.

%setup -q -c -T

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}



%install
cd %{name}-%{version}
rm -rf %{buildroot}
cmake .
make DESTDIR=%{buildroot} INSTALL="install -p" install

install -d -m 0755 %{buildroot}/usr/lib
install -d -m 0755 %{buildroot}%{_includedir}
%__mv %{buildroot}/usr/local/include/leatherman %{buildroot}%{_includedir}
%__mv %{buildroot}/usr/local/lib/* %{buildroot}/usr/lib
%__rm -rf %{buildroot}/usr/local

%{__sed} -i -e 's/%dir ""//g' filelist
%{__sed} -i -e '/^$/d' filelist

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%defattr(-,root,root,-)
%dir /usr/lib/cmake
%dir /usr/lib/cmake/leatherman
/usr/lib/cmake/*
/usr/lib/%{name}*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

%changelog
