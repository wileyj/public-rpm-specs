%define realname tomcat-connectors
%define major 1
Name: mod_jk
Version: %{major}.2.27
Release: 4.%{dist}
License: Apache 2.0
Vendor: %{vendor}
Packager: %{packager}
Summary:    mod_jk for Apache >= 2.2
Group:          System Environment/Daemons
Requires:   httpd
AutoReq:  0
BuildRequires:	 apr-devel, apr-util-devel, apr, apr-util
BuildRequires:	 httpd-tools
BuildRequires:   httpd >= 2.2
BuildRequires:   httpd-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source: %{realname}-%{version}-src.tar.gz
Provides: mod_jk = 0:%{version}-%{release}
%define _apache_dir /etc/httpd

%description
mod_jk for apache v2.2

%prep
%setup -qn %{realname}-%{version}-src
%build

function build_mod_jk()
{
	apache=$1; shift
	ls -al $apache/bin/apxs
	ls -al /usr/bin/apu-1-config
	ls -al /usr/bin/apr-1-config
	export PATH=$PATH:$apache/bin/
	cd native
	%{configure} --with-apxs=$apache/bin/apxs --with-apu=/usr/bin/apu-1-config --with-apr=/usr/bin/apr-1-config
	make
	find .
}

function install_mod_jk()
{
	apache=$1; shift
	mkdir -p $RPM_BUILD_ROOT$apache/modules
	cp apache-2.0/mod_jk.so $RPM_BUILD_ROOT$apache/modules
}

build_mod_jk %{_apache_dir}
install_mod_jk %{_apache_dir}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files 
%defattr(-, root, root)
%{_apache_dir}/modules/mod_jk.so
