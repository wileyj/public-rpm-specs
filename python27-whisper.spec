%{!?python27_sitelib: %global python27_sitelib %(%{__python27} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%include %{_rpmconfigdir}/macros.d/macros.python27
%global srcname whisper

Name:           python27-%{srcname}
Version:        0.9.10
Release:        1.%{dist}
Summary:        Fixed size round-robin style database
Group:          Applications/Databases
License:        Apache Software License 2.0
Packager: %{packager}
Vendor: %{vendor}
URL:            https://launchpad.net/graphite
Source0:        https://github.com/downloads/graphite-project/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27 python27-devel python27-setuptools
Requires:       python27

%description
Whisper is a fixed-size database, similar in design to RRD.  It provides fast,
reliable storage of numeric data over time.

%prep
%setup -q -n %{srcname}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python27} -c 'import setuptools; execfile("setup.py")' build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%{__python27} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{srcname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}-%{version}
[ "%{_builddir}/%{srcname}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}

%files
%defattr(-,root,root,-)

%{python27_sitelib}/*
/usr/bin/*

%changelog
