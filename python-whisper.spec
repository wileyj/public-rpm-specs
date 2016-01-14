
%include %{_rpmconfigdir}/macros.d/macros.python
%global srcname whisper

Name:           python-%{srcname}
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
BuildArch:      noarch

BuildRequires:  python python-devel python-setuptools
Requires:       python

%description
Whisper is a fixed-size database, similar in design to RRD.  It provides fast,
reliable storage of numeric data over time.

%prep
%setup -q -n %{srcname}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} -c 'import setuptools; execfile("setup.py")' build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)

%{python_sitelib}/*
/usr/bin/*

%changelog
