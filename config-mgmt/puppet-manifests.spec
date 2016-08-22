%define _prefix	/etc/puppetlabs
%define env prod
%define epoch %(date +%s)

Name:		%{env}-puppet
Version:	%{epoch}
Release:	%{dist}
Summary:	puppet manigests
Source1:	ops-puppet
Group:		Development/Tools/Building
License:	GPL
Vendor: 	%{vendor}
Packager: 	%{packager}
Requires:	puppet at
BuildArch:      noarch

%description
%{summary} build %{epoch}



%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
cp -R %SOURCE1 .

%build
find . -name ".DS_Store" -exec rm -rf {} \; 
find . -name ".git" -exec rm -rf {} \; 
cd ops-puppet

%install
cd ops-puppet
rm -rf %{buildroot}

%__install -d %{buildroot}%{_prefix}
cp -R scripts %{buildroot}%{_prefix}
cp -R code %{buildroot}%{_prefix}
cp -R facter %{buildroot}%{_prefix}
%__install -D -m0644 puppet/puppet.conf %{buildroot}%{_prefix}/puppet/puppet.conf
%__install -D -m0644 puppet/puppetdb.conf %{buildroot}%{_prefix}/puppet/puppetdb.conf
%__install -D -m0644 puppet/routes.yaml %{buildroot}%{_prefix}/puppet/routes.yaml

%post -p /bin/bash
echo "Executing Puppet..."
nohup bash -c "sleep 5; /etc/puppetlabs/scripts/run-puppet-local &"  
#/sbin/service atd force-reload
#at now+1 minutes -f %{_prefix}/scripts/run-puppet-local

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%dir %{_prefix}/scripts
%dir %{_prefix}/code
%dir %{_prefix}/facter
%config(noreplace) %{_prefix}/puppet/puppet.conf
%config(noreplace) %{_prefix}/puppet/puppetdb.conf
%config(noreplace) %{_prefix}/puppet/routes.yaml
%{_prefix}/code/*
%attr(0755,root,root) %{_prefix}/scripts/*
%{_prefix}/facter/*

%changelog
