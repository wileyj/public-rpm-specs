%include %{_rpmconfigdir}/macros.d/macros.python27
%global srcname sphinx
%global tarname Sphinx

Name:           python27-%{srcname}
Version:        1.3.1
Release:        1.%{dist}
Summary:        Python documentation generator 
Group:          Development/Languages
License:        BSD
Packager: %{packager}
Vendor: %{vendor}
URL:            http://pypi.python.org/pypi/sphinx
Source0:        %{tarname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
Requires:       python27

%description
Sphinx is a tool that makes it easy to create intelligent and beautiful documentation for Python projects (or other documents consisting of multiple reStructuredText sources), written by Georg Brandl. 
It was originally created for the new Python documentation, and has excellent facilities for Python project documentation, but C/C++ is supported as well, and more languages are planned.

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
%{python27_sitelib}/%{srcname}/
%{python27_sitelib}/%{tarname}*.egg-info
%{_bindir}/sphinx-apidoc
%{_bindir}/sphinx-autogen
%{_bindir}/sphinx-build
%{_bindir}/sphinx-quickstart

%changelog

