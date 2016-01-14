%include %{_rpmconfigdir}/macros.d/macros.python27
%global srcname twisted-core
%global tarname Twisted
%global pkgname twisted

Name:           python27-%{srcname}
Version:        15.2.1
Release:        1.%{dist}
Summary:        Distributed Task Queue 
Group:          Development/Languages
License:        BSD
Packager: %{packager}
Vendor: %{vendor}
URL:            http://pypi.python.org/pypi/redis
Source0:        %{tarname}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27 python27-devel
BuildRequires:  python27-setuptools
Requires:       python27

%description
The Python interface to the Redis key-value store.

%prep
%setup -q -n %{tarname}-%{version}

%build
%{__python27} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python27} setup.py install --skip-build --root $RPM_BUILD_ROOT
 
%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{srcname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}-%{version}
[ "%{_builddir}/%{srcname}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}

%files
%defattr(-,root,root,-)
%doc LICENSE
%{python27_sitearch}/%{pkgname}/
%{python27_sitearch}/%{tarname}*.egg-info
%{_bindir}/cftp
%{_bindir}/ckeygen
%{_bindir}/conch
%{_bindir}/lore
%{_bindir}/mailmail
%{_bindir}/manhole
%{_bindir}/pyhtmlizer
%{_bindir}/tap2deb
%{_bindir}/tap2rpm
%{_bindir}/tkconch
%{_bindir}/trial
%{_bindir}/twistd

%changelog

