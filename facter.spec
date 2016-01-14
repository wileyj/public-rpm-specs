%global factpath /etc/puppetlabs/facter/facts.d
%global binpath  /opt/puppetlabs/bin

Name:           facter
Version:        3.1.3
Release:        1.%{dist}
Summary:        Command and ruby library for gathering system information
Group:          System Environment/Base
License:        ASL 2.0
Vendor: 	%{vendor}
Packager: 	%{packager}
URL:            https://puppetlabs.com/%{name}
Source0:        %{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: boost-devel >= 1.59
BuildRequires: openssl-devel libblkid-devel libcurl-devel gcc-c++ make wget tar libyaml libyaml-devel  leatherman yaml-cpp-devel
Requires:       dmidecode
Requires:       pciutils
Requires:       virt-what
Requires:       net-tools
Requires:       which

%description
Facter is a lightweight program that gathers basic node information about the
hardware and operating system. Facter is especially useful for retrieving
things like operating system names, hardware characteristics, IP addresses, MAC
addresses, and SSH keys.

Facter is extensible and allows gathering of node information that may be
custom or site specific. It is easy to extend by including your own custom
facts. Facter can also be used to create conditional expressions in Puppet that
key off the values returned by facts.

%prep
%setup -q -n %{name}

%build
git pull
git submodule init
git submodule update

%install
rm -rf %{buildroot}
%__mkdir_p release
pwd
cd release
cmake ..
make DESTDIR=%{buildroot} INSTALL="install -p" install

# Create directory for external facts
%__mkdir_p %{buildroot}%{factpath}
%__mkdir_p %{buildroot}%{binpath}
ln -sf %{_bindir}/%{name} ${RPM_BUILD_ROOT}%{binpath}/%{name}


install -D -pv -m 644 man/man8/%{name}.8 %{buildroot}/%{_mandir}/man8/%{name}.8

%postun
if [ "$1" -ge 1 ]; then
  /sbin/service puppet condrestart >/dev/null 2>&1 || :
fi


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}


%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/%{name}
%dir %{factpath}
%{facter_libdir}/%{name}*
%{_mandir}/man8/%{name}*
%{binpath}/%{name}

%changelog
