%global _python_bytecompile_errors_terminate_build 0
%include %{_rpmconfigdir}/macros.d/macros.rubygems
%global _plugin puppet-agent
%define repo https://github.com/puppetlabs/mcollective-puppet-agent.git
%define gitversion %(echo `curl -s https://github.com/puppetlabs/mcollective-puppet-agent/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?amzn} >= 1
%global mco_libdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorlibdir"]')
%else
%global mco_libdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["sitelibdir"]')
%endif

%global mco_prefix /opt/mcollective
%global mco_bindir %{mco_prefix}/bin
%global mco_sbindir %{mco_prefix}/sbin
%global mco_confdir %{mco_prefix}/etc
%global mco_plugindir %{mco_prefix}/plugins

Name:           mco-puppet-agent
Version:        %{gitversion}
Release:        1.%{dist}
Summary:        MCollective Agent to manage the Puppet Agent
License:        ASL 2.0
Packager:       %{packager}
Vendor:         %{vendor}
URL:            http://puppetlabs.com
Group:          System Environment/Base
BuildRequires:  ruby >= 2.2 git 
Requires:       ruby >= 2.2 puppet facter hiera mcollective-agent
BuildArch:      noarch

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
%__mkdir_p %{buildroot}/%{mco_plugindir}/%{_plugin}/agent
%__mkdir_p %{buildroot}/%{mco_plugindir}/%{_plugin}/data
%__mkdir_p %{buildroot}/%{mco_plugindir}/%{_plugin}/util
%__mkdir_p %{buildroot}/%{mco_plugindir}/%{_plugin}/validator

cp -pa agent/* %{buildroot}/%{mco_plugindir}/%{_plugin}/data/
cp -pa util/* %{buildroot}/%{mco_plugindir}/%{_plugin}/util/
cp -pa agent/* %{buildroot}/%{mco_plugindir}/%{_plugin}/agent/
cp -pa validator/* %{buildroot}/%{mco_plugindir}/%{_plugin}/validator/



%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%dir %{mco_plugindir}/%{_plugin}
%{mco_plugindir}/%{_plugin}/*
