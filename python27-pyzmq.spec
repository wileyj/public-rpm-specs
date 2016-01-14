%global srcname pyzmq
%global shortname zmq
%include %{_rpmconfigdir}/macros.d/macros.python27

Name:           python27-%{srcname}
Version:        15.1.0
Release:        1.rtg
Summary:        Python bindings for 0MQ
Group:          Development/Languages
License:        BSD
Packager:       Rising Tide Games
Vendor:         Rising Tide Games
URL:            http://pypi.python.org/pypi/tdb
Source0:        %{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
Requires:       python27

%description
PyZMQ is the official Python binding for the ZeroMQ Messaging Library (http://www.zeromq.org)

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
%dir %{_libdir}/python2.7/dist-packages/%{shortname}
%{_libdir}/python2.7/dist-packages/%{shortname}/*
%{_libdir}/python2.7/dist-packages/%{srcname}*.egg-info

%changelog

