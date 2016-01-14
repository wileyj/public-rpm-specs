%{!?python27_sitelib: %global python27_sitelib %(%{__python27} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%include %{_rpmconfigdir}/macros.d/macros.python27
%global srcname augeas

Name:           python-%{srcname}
Version:        0.4.0
Release:        1.%{dist}
Summary:        python augeas

Group:          Development/Languages
License:        BSD
Packager: %{packager}
Vendor: %{vendor}
URL:            http://pypi.python.org/pypi/augeas
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python27-devel
BuildRequires:  python27-setuptools

Requires:       python27


%description
python augeas

%prep
%setup -q -n %{name}-%{version}


%build
%{__python27} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python27} setup.py install --skip-build --root $RPM_BUILD_ROOT

 
%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{python27_sitelib}/%{srcname}*
%{python27_sitelib}/python_%{srcname}*.egg-info

%changelog

