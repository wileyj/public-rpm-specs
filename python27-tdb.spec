%global srcname tdb
%include %{_rpmconfigdir}/macros.d/macros.python27


Name:           python27-%{srcname}
Version:        1.3.5
Release:        1.rtg
Summary:        Distributed Task Queue 

Group:          Development/Languages
License:        BSD
Packager:       Rising Tide Games
Vendor:         Rising Tide Games
URL:            http://pypi.python.org/pypi/tdb
Source0:        %{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
Requires:       python27

%description
This is a simple database API

%prep
%setup -q -n %{srcname}-%{version}


%build
#%{_python27} setup.py build
%{_configure}
%__make

%install
rm -rf $RPM_BUILD_ROOT
%{_python27} setup.py install --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE
%{python27_sitelib}/%{srcname}/
%{python27_sitelib}/%{srcname}*.egg-info

%changelog

