%define short_name cloudwatch_exporter
%define repo https://github.com/prometheus/%{short_name}
%define gitversion %(echo `curl -s %{repo}/releases | grep 'span class="tag-name"' | head -1 | tr -d '</span class="tag-name">cloudwatchexporter_-'`)
%define gitsummary %(echo `curl -s %{repo} | grep 'meta name="description" content="' | head -1 | cut -d'"' -f4`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define exporter_prefix /opt/prometheus/exporters/%{short_name}
%define release_ver 1

Name:           prometheus-%{short_name}
Version:        %{gitversion}
Release:        %{release_ver}.%{revision}.%{?dist}
Summary:        %{gitsummary}
License:        ASL 2.0
URL:            %{repo}
BuildArch:      noarch
BuildRequires:  maven
Requires:	jdk
Provides:               prometheus-cloudwatch_exporter

%description
%{summary}

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}

%build
cd %{name}-%{version}
mvn package


%install
cd %{name}-%{version}
%__mkdir -p %{buildroot}%{exporter_prefix}
%__cp -pa * %{buildroot}%{exporter_prefix}/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%%{name}-contrib-%{version}" != "/" ] && %__rm -rf %{_builddir}/%%{name}-contrib-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{pkgname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pkgname}-%{version}

%files 
%dir %{exporter_prefix}
%{exporter_prefix}/*


%changelog
