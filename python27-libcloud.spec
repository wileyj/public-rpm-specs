%global srcname libcloud
%include %{_rpmconfigdir}/macros.d/macros.python27

Name:           python27-%{srcname}
Version:        0.19.0
Release:        1.rtg
Summary:        A standard Python library that abstracts away differences among multiple cloud provider API 
Group:          Development/Languages
License:        BSD
Packager:       %{packager}
Vendor:         %{vendor}
URL:            http://pypi.python.org/pypi/apache-libcloud
Source0:        apache-%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
Requires:       python27

%description
Apache Libcloud is a Python library which hides differences between different cloud provider APIs and allows you to manage different cloud resources through a unified and easy to use API.
Resources you can manage with Libcloud are divided into the following categories:

%prep
%setup -q -n apache-%{srcname}-%{version}

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
%{python27_sitelib}/%{srcname}
%{python27_sitelib}/%{srcname}/*
%{python27_sitelib}/apache_%{srcname}*.egg-info

%changelog

