%global srcname argparse
%include %{_rpmconfigdir}/macros.d/macros.python27

Name:           python27-%{srcname}
Version:        1.4.0
Release:        1.rtg
Summary:        Python command-line parsing library
Group:          Development/Languages
License:        BSD
Packager:       %{packager}
Vendor:         %{vendor}
URL:            http://pypi.python.org/pypi/argparse
Source0:        %{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
Requires:       python27

%description
Python command-line parsing library

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
%{python27_sitelib}/%{srcname}*

%changelog

