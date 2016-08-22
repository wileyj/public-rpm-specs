%define library_name libyaml-cpp
Name:           yaml-cpp
Version:        0.5.2
Release:        13.2.%{dist}
Summary:        YAML parser and emitter in C++
License:        MIT
Group:          Development/Libraries/C and C++
Url:            https://github.com/jbeder/yaml-cpp/
Source:         %{name}.tar.gz
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  sed
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
A YAML parser and emitter in C++ matching the YAML 1.2 spec.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       boost-devel

%description devel
Development files for %{name} library.

%prep
%setup -q -n %{name}

%build
git pull

%install
%cmake .
make DESTDIR=%{buildroot} INSTALL="install -p" install

%post -n %{name} -p /sbin/ldconfig
%postun -n %{name} -p /sbin/ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files 
%defattr(-,root,root,-)
%{_libdir}/%{library_name}.*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/%{name}-*.cmake

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}/node
%dir %{_includedir}/%{name}/node/detail
%dir %{_includedir}/%{name}/contrib
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/node/*.h
%{_includedir}/%{name}/contrib/*.h
%{_includedir}/%{name}/node/detail/*.h

%changelog
