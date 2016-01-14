%include %{_rpmconfigdir}/macros.d/macros.python27
%global srcname pip

Name:           python27-%{srcname}
Version:        7.1.2
Release:        1.%{dist}
Url:            http://www.pip-installer.org
Summary:        Pip installs packages. Python packages. An easy_install replacement
License:        MIT
Packager: %{packager}
Vendor: %{vendor}
Group:          Development/Languages/Python
Source:         http://pypi.python.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python27
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
Requires:       python27-setuptools

%description
Pip is a replacement for easy_install. It uses mostly the same techniques for
finding packages, so packages that were made easy_installable should be
pip-installable as well.

%prep
%setup -q -n %{srcname}-%{version}
sed -i "s|#!/usr/bin/env python||g" pip/__init__.py # Fix non-executable script

%build
%{__python27} setup.py build

%install
%{__python27} setup.py install --prefix=%{_prefix} --root=%{buildroot}
rm %{buildroot}%{_bindir}/%{srcname}
ln -s %{_bindir}/%{srcname}%{py27_ver} %{buildroot}%{_bindir}/%{srcname}

%pre
# Since /usr/bin/pip became ghosted to be used with update-alternatives, we have to get rid
# of the old binary resulting from the non-update-alternativies-ified package:
[[ ! -L %{_bindir}/%{srcname} ]] && rm -f %{_bindir}/%{srcname}
exit 0

%post
update-alternatives --install %{_bindir}/%{srcname} %{srcname} %{_bindir}/%{srcname}%{py27_ver} 30

%preun
if [ $1 -eq 0 ] ; then
    update-alternatives --remove %{srcname} %{_bindir}/%{srcname}%{py27_ver}
fi

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{srcname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}-%{version}
[ "%{_builddir}/%{srcname}" != "/" ] && %__rm -rf %{_builddir}/%{srcname}

%files
%defattr(-,root,root,-)
%doc AUTHORS.txt CHANGES.txt LICENSE.txt README.rst
%ghost %{_bindir}/%{srcname}
%{_bindir}/%{srcname}2.7
%{_bindir}/%{srcname}
%{_bindir}/%{srcname}2
%{python27_sitelib}/%{srcname}*.egg-info
%{python27_sitelib}/%{srcname}

%changelog
