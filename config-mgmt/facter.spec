%global factpath /etc/puppetlabs/facter/facts.d
%define repo https://github.com/puppetlabs/facter
%define gitversion %(echo `curl -s  %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Name:           facter
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
Summary:        Command and ruby library for gathering system information
Group:          System Environment/Base
License:        ASL 2.0
Vendor: 	%{vendor}
Packager: 	%{packager}
URL:            https://puppetlabs.com/%{name}
Patch0:		facter-ruby-2.3.patch
#Patch1:        facter-2.3.0.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires: boost-devel >= 1.59 cpp-hocon cpp-hocon-devel
#BuildRequires: openssl-devel libblkid-devel libcurl-devel gcc-c++ make wget tar libyaml libyaml-devel  leatherman yaml-cpp-devel
#BuildRequires: rapidjson-devel
BuildRequires:  boost-system >= 1.63.0
BuildRequires:  boost-thread >= 1.63.0
BuildRequires:  boost-filesystem >= 1.63.0
BuildRequires:  boost-regex >= 1.63.0
BuildRequires:  boost-date-time >= 1.63.0
BuildRequires:  boost-timer >= 1.63.0
BuildRequires:  boost-locale >= 1.63.0
BuildRequires:  boost-random >= 1.63.0
BuildRequires:  boost-serialization >= 1.63.0
BuildRequires:  boost-iostreams >= 1.63.0
BuildRequires:  boost-signals >= 1.63.0
BuildRequires:  boost-math >= 1.63.0
BuildRequires:  boost >= 1.63.0
BuildRequires:  boost-devel >= 1.63.0
BuildRequires:  cpp-hocon >= 0.1.4
BuildRequires:  yaml-cpp >= 0.5.2
BuildRequires:  yaml-cpp-devel >= 0.5.2
BuildRequires:  leatherman >= 0.10.1
BuildRequires:  leatherman-devel >= 0.10.1
BuildRequires:  rapidjson >= 1.1.0
BuildRequires:  rapidjson-devel >= 1.1.0
BuildRequires:  libuuid >= 2.23.2
BuildRequires:  libgcc >= 4.8.5
BuildRequires:  libstdc++ >= 4.8.5
BuildRequires:  libstdc++-devel >= 4.8.5
BuildRequires:  libblkid >= 2.23.2
BuildRequires:  libblkid-devel >= 2.23.2
BuildRequires:  openssl-libs >= 1.0.1e
BuildRequires:  openssl-devel >= 1.0.1e
BuildRequires:  cpp-hocon-devel >= 0.1.4
BuildRequires:  gcc-c++ >= 4.8.5
BuildRequires:  gcc >= 4.8.5
BuildRequires:  cpp >= 4.8.5
BuildRequires:  make >= 3.82
BuildRequires:  cmake >= 3.6.1
BuildRequires:  wget tar libcurl-devel libyaml libyaml-devel
Requires:      dmidecode pciutils virt-what net-tools which rubygem-semantic_puppet cpp-hocon leatherman

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
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
#git checkout -b stable
git checkout tags/3.4.1

#%patch0

%build
cd %{name}-%{version}

%install
cd %{name}-%{version}
rm -rf %{buildroot}
%__mkdir_p release
pwd
cd release
export CLASSPATH="$CLASSPATH:%{_builddir}/%{name}-%{version}/release/lib"
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DRUBY_INCLUDE_DIR=/usr/include/ruby -DRUBY_LIBRARY=/usr/lib64/ruby ..
make DESTDIR=%{buildroot} INSTALL="install -p" install

#export CLASSPATH="/usr/java/current/lib:/opt/rpmbuild/BUILD/%{name}-%{version}/release/lib"
#cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DRUBY_INCLUDE_DIR=/usr/include/ruby -DRUBY_LIBRARY=/usr/lib64/ruby ..
#make DESTDIR=/opt/rpmbuild/BUILDROOT/facter-3.4.1-1.local.el7.x86_64 'INSTALL=install -p' install

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
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
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
