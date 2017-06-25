%global _python_bytecompile_errors_terminate_build 0
#%include %{_rpmconfigdir}/macros.d/macros.rubygems
%global _plugin nettest-agent
%define repo https://github.com/puppetlabs/mcollective-%{_plugin}
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?amzn} >= 1
%global mco_libdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorlibdir"]')
%else
%global mco_libdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["sitelibdir"]')
%endif
%define gitversion 1.0.0
%global mco_prefix /opt/mcollective
%global mco_bindir %{mco_prefix}/bin
%global mco_sbindir %{mco_prefix}/sbin
%global mco_confdir %{mco_prefix}/etc
%global mco_plugindir %{mco_prefix}/plugins


Summary:   MCollective Agent to manage the Puppet Agent
Name:      mcollective-%{_plugin}
Version:   %{gitversion}
Release: %{rel_version}.%{revision}.%{dist}
Vendor:    %{vendor}
Packager:  %{packager}
License:   ASL 2.0
URL:       https://github.com/puppetlabs/mcollective-package-agent
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Group:     System Tools
Requires:  mcollective-common >= 2.2.1

%description
%{summary}

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
%{__install} -d -m0755 %{buildroot}%{mco_plugindir}/%{_plugin}
cp -a agent aggregate application data util validator %{buildroot}%{mco_plugindir}/%{_plugin}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%dir %{mco_plugindir}/%{_plugin}
%{mco_plugindir}/%{_plugin}/*

%changelog
