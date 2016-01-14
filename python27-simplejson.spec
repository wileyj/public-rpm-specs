%include %{_rpmconfigdir}/macros.d/macros.python27
%global srcname simplejson

Name:           python27-%{srcname}
Version:        3.8.1
Release:        1.%{dist}
Summary:        Simple, fast, extensible JSON encoder/decoder for Python
Group:          Development/Languages
License:        BSD
Packager: %{packager}
Vendor: %{vendor}
URL:            http://pypi.python.org/pypi/simplejson
Source0:        %{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27 python27-devel
BuildRequires:  python27-setuptools
Requires:       python27

%description
Simple, fast, extensible JSON encoder/decoder for Python

%prep
%setup -q -n %{srcname}-%{version}

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
%{python27_sitearch}/%{srcname}
%{python27_sitearch}/%{srcname}*.egg-info

%changelog

