%include %{_rpmconfigdir}/macros.d/macros.python27
%global srcname setuptools

Name:           python27-setuptools
Version:        18.6
Release:        1.%{dist}
Summary:        Easily build and distribute Python packages
Group:          Applications/System
License:        Python or ZPLv2.0
Packager: %{packager}
Vendor: %{vendor}
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/d/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:        psfl.txt
Source2:        zpl.txt
BuildRoot:      %{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27-devel, python27
Provides: python27-setuptools-devel = %{version}-%{release}

%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

This package contains the distribute fork of setuptools.

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
%doc *.txt docs
%{python27_sitelib}/*
%{_bindir}/easy_install
%{_bindir}/easy_install-2.*

%changelog
