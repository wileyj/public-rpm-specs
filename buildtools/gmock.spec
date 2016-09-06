%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

Summary:        Google C++ Mocking Framework
Name:           gmock
Version:        1.6.0
Release:        4.%{dist}
License:        BSD
Vendor: %{vendor}
Packager: %{packager}
Group:          System Environment/Libraries
URL:            http://code.google.com/p/googlemock/
Source0:        gmock-1.6.0.zip
Patch0:         install.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
BuildRequires:  gtest-devel >= 1.6.0
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
Requires:       gtest >= 1.6.0

%description
Inspired by jMock, EasyMock, and Hamcrest, and designed with C++'s
specifics in mind, Google C++ Mocking Framework (or Google Mock for
short) is a library for writing and using C++ mock classes.

Google Mock:

 o lets you create mock classes trivially using simple macros,
 o supports a rich set of matchers and actions,
 o handles unordered, partially ordered, or completely ordered
   expectations,
 o is extensible by users, and
 o works on Linux, Mac OS X, Windows, Windows Mobile, minGW, and
   Symbian.

%package        devel
Summary:        Development files for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%setup -q
%patch0 -p1

%build
# needed for mahe check to work without failures
autoreconf -fvi     
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install INSTALL="%{__install} -p" DESTDIR=%{buildroot}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc CHANGES CONTRIBUTORS COPYING README

%files devel
%defattr(-, root, root, -)
%{_bindir}/gmock-config
%{_includedir}/../src/%{name}/
%{_includedir}/%{name}/
%{_datadir}/pkgconfig/*
%{_datadir}/%{name}/generator/

%changelog
