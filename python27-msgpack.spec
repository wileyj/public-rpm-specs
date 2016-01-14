%global srcname msgpack
%include %{_rpmconfigdir}/macros.d/macros.python27

Name:           python27-%{srcname}
Version:        0.4.6
Release:        1.rtg
Summary:        MessagePack (de)serializer.
Group:          Development/Languages
License:        BSD
Packager:       %{packager}
Vendor:         %{vendor}
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        %{srcname}-python-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27-devel
BuildRequires:  python27-setuptools
Requires:       python27

%description
MessagePack is a fast, compact binary serialization format, suitable for similar data to JSON. This package provides CPython bindings for reading and writing MessagePack data.

%prep
%setup -q -n %{srcname}-python-%{version}

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
%{_libdir}/python2.7/dist-packages/%{srcname}
%{_libdir}/python2.7/dist-packages/%{srcname}/*
%{_libdir}/python2.7/dist-packages/%{srcname}*.egg-info

%changelog

