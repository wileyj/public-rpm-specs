%global factpath /etc/puppetlabs/facter/facts.d
%define repo https://github.com/puppetlabs/facter.git

Name:           facter
Version:        3.1.3
Release:        1.%{dist}
Summary:        Command and ruby library for gathering system information
Group:          System Environment/Base
License:        ASL 2.0
Vendor: 	%{vendor}
Packager: 	%{packager}
URL:            https://puppetlabs.com/%{name}
#Source0:        %{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: boost-devel >= 1.59
BuildRequires: openssl-devel libblkid-devel libcurl-devel gcc-c++ make wget tar libyaml libyaml-devel  leatherman yaml-cpp-devel
Requires:      dmidecode pciutils virt-what net-tools which

%description
Facter is a lightweight program that gathers basic node information about the
hardware and operating system. Facter is especially useful for retrieving
things like operating system names, hardware characteristics, IP addresses, MAC
addresses, and SSH keys.

Facter is extensible and allows gathering of node information that may be
custom or site specific. It is easy to extend by including your own custom
facts. Facter can also be used to create conditional expressions in Puppet that
key off the values returned by facts.


%setup -q -c -T
%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}

%install
cd %{name}-%{version}
rm -rf %{buildroot}
%__mkdir_p release
pwd
cd release
export CLASSPATH="$CLASSPATH:%{_builddir}/%{name}-%{version}/release/lib"
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} ..
make DESTDIR=%{buildroot} INSTALL="install -p" install

# Create directory for external facts
%__mkdir_p %{buildroot}%{factpath}
%__mkdir_p %{buildroot}%{_bindir}
install -D -pv -m 644 %{_builddir}/%{name}-%{version}/man/man8/%{name}.8 %{buildroot}/%{_mandir}/man8/%{name}.8

%postun -p /sbin/ldconfig
if [ "$1" -ge 1 ]; then
  /sbin/service puppet condrestart >/dev/null 2>&1 || :
fi

%post -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%dir %{factpath}
%{_mandir}/man8/%{name}*
%{_datarootdir}/ruby/vendor_ruby/facter.rb
%{_prefix}/lib/lib%{name}*
%{_includedir}/%{name}/
%{_datarootdir}/ruby/vendor_ruby/facter.jar

%changelog
