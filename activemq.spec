%define _prefix /opt/%{name}

Name:           activemq
Summary:        Apache ActiveMQ
Version:        5.13.3 
Release:	1.%{dist}
Url:            http://activemq.apache.com
License:        ASL
Vendor: %{vendor}
Packager: %{packager}
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Source0:	apache-%{name}-%{version}-bin.tar.gz 
Provides:	%{name} = %{version}

%description
Apache activemq

%prep
%setup -n apache-%{name}-%{version} -T -b 0
%build
%install
rm -rf %{buildroot}
%__mkdir_p %{buildroot}%{_prefix}
%__mkdir_p %{buildroot}%{_bindir}
cp -R * %{buildroot}%{_prefix}/

ln -sf %{_prefix}/bin/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%post
ldconfig -a

%postun
rm -f %{_prefix}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%{_prefix}
%{_bindir}/%{name}


